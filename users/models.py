from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Lesson, Course

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


class Payment(models.Model):
    """Модель оплаты"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты', **NULLABLE)
    payment_method = models.CharField(max_length=100, verbose_name='способ оплаты', choices=[('cash', 'Наличные'),
                                                                                             ('transfer',
                                                                                              'Перевод на счет')])

    def __str__(self):
        return f'Платеж от {self.user} на сумму {self.amount} руб.'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
        ordering = ['-payment_date']

