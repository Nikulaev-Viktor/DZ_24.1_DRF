from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ('payment_method',)
    filterset_fields = ('payment_date', 'payment_method', 'paid_course', 'paid_lesson',)
    ordering_fields = ('payment_date',)


class UserAPICreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
