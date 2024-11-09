from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import ValidateLink


class LessonSerializer(ModelSerializer):
    validators = [ValidateLink(field='link')]

    class Meta:
        model = Lesson
        fields = '__all__'

    class SubscriptionSerializer(ModelSerializer):
        class Meta:
            model = Subscription
            fields = '__all__'


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    subscription = SerializerMethodField()

    def get_subscription(self, instance):  # Rename method here
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=instance).exists()

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    lessons_count = SerializerMethodField()


    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'preview', 'lessons_count', 'lessons',)


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'user', 'course', 'subscription_status',)
