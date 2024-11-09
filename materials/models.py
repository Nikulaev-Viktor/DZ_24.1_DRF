from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', help_text='введите название')
    description = models.TextField(verbose_name='Описание', help_text='введите описание')
    preview = models.ImageField(upload_to='materials/image', verbose_name='Изображение', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name='Кто создал курс',
                              **NULLABLE
                              )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', help_text='выберите курс')
    title = models.CharField(max_length=100, verbose_name='Название', help_text='введите название')
    description = models.TextField(verbose_name='Описание', help_text='введите описание')
    preview = models.ImageField(upload_to='materials/image', verbose_name='Изображение', **NULLABLE)
    link = models.URLField(max_length=200, verbose_name='Видео', help_text='введите ссылку на видео', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name='Кто создал урок',
                              **NULLABLE
                              )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE, related_name="subscription_course")
    subscription_status = models.BooleanField(default=False, verbose_name='Статус подписки')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
