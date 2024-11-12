import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import Payment, User
from users.permissions import IsModer, IsOwner
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_stripe_price, create_stripe_product, create_stripe_session


class PaymentListAPIView(ListAPIView):
    """Эндпоинт для получения списка платежей"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ('payment_method',)
    filterset_fields = ('payment_date', 'payment_method', 'paid_course', 'paid_lesson',)
    ordering_fields = ('payment_date',)


class PaymentCreateAPIView(CreateAPIView):
    """Эндпоинт для создания нового платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        try:
            # Создаем продукт, цену и сессию в Stripe
            product_id = create_stripe_product(payment)
            price_id = create_stripe_price(payment.amount, product_id)
            session_id, payment_url = create_stripe_session(price_id)

            # Сохраняем session_id и ссылку на оплату в базе данных
            payment.session_id = session_id
            payment.payment_link = payment_url
            payment.save()

        except stripe.error.StripeError as e:
            # Логирование ошибки и возвращение информативного сообщения
            raise ValidationError(f"Ошибка при создании платежа в Stripe: {e.user_message}")


class UserCreateAPIView(CreateAPIView):
    """Эндпоинт для создания нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """Эндпоинт для получения списка пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """Эндпоинт для получения информации о пользователе"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class UserUpdateAPIView(UpdateAPIView):
    """Эндпоинт для изменения информации о пользователе"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class UserDeleteAPIView(DestroyAPIView):
    """Эндпоинт для удаления пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
