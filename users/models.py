from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователей"""
    username = None

    first_name = models.CharField(max_length=100, verbose_name='имя')
    email = models.EmailField(unique=True, verbose_name='email', help_text='введите email')
    phone_number = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE,
                                    help_text='введите номер телефона')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='аватар', **NULLABLE,
                               help_text='загрузите свой аватар')
    city = models.CharField(max_length=100, verbose_name='Город', **NULLABLE, help_text='введите город')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

