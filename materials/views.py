from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer, SubscriptionSerializer)
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
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

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated, ~IsModer,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (IsAuthenticated,  IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]


from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .models import Subscription, Course
from .serializers import SubscriptionSerializer
from django.shortcuts import get_object_or_404

class SubscriptionCreateAPIView(CreateAPIView):
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
            status_code = status.HTTP_201_CREATED  # Return 201 when a resource is created

        return Response({"message": message}, status=status_code)









