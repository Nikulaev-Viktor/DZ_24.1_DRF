from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from materials.tasks import send_email_about_update_course
from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer, SubscriptionSerializer)
from users.permissions import IsModer, IsOwner
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class CourseViewSet(ModelViewSet):
    """ViewSet управление курсами."""
    queryset = Course.objects.all()
    pagination_class = CustomPagination
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        updated_course = serializer.save()
        send_email_about_update_course.delay(updated_course.id)


    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated, ~IsModer,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (IsAuthenticated, IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """Эндпоинт создания урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    """Эндпоинт получения списка уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonRetrieveAPIView(RetrieveAPIView):
    """Эндпоинт получения одного урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    """Эндпоинт обновления урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    """Эндпоинт удаления урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]


class SubscriptionCreateAPIView(CreateAPIView):
    """Эндпоинт создания подписки."""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            # If subscription exists, delete it
            subs_item.delete()
            message = 'Подписка удалена'
            status_code = status.HTTP_200_OK
        else:
            # If subscription doesn't exist, create it
            Subscription.objects.create(user=user, course=course_item, subscription_status=True)
            message = 'Подписка добавлена'
            status_code = status.HTTP_201_CREATED

        return Response({"message": message}, status=status_code)
