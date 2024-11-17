from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription, Course
from datetime import timedelta
from django.utils import timezone

from users.models import User


@shared_task
def send_email_about_update_course(course_id):
    """Отправка письма об обновлении курса."""
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course)
    for subscription in subscriptions:
        send_mail(
            subject="Обновление материалов курса",
            message=f"Курс '{course.title}' был обновлён.",
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )


@shared_task
def block_user():
    now = timezone.now()
    users = User.objects.filter(
        Q(last_login__lte=now - timedelta(days=30)) | Q(last_login__isnull=True),
        is_active=True
    )
    for user in users:
        user.is_active = False
        user.save()
