# Generated by Django 5.1.2 on 2024-11-11 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_link',
            field=models.URLField(blank=True, help_text='введите ссылку на оплату', max_length=400, null=True, verbose_name='ссылка на оплату'),
        ),
        migrations.AddField(
            model_name='payment',
            name='session_id',
            field=models.CharField(blank=True, help_text='введите идентификатор сессии', max_length=255, null=True, verbose_name='идентификатор сессии'),
        ),
    ]