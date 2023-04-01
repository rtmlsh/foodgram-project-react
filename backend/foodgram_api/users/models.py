from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель, описывающая пользователя"""
    username = models.CharField(verbose_name='Имя пользователя', max_length=256, unique=True)
    email = models.EmailField(verbose_name='Электронная почта', max_length=256, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=256, unique=True)
    second_name = models.CharField(verbose_name='Фамилия', max_length=256, unique=True)
    is_subscribed = models.BooleanField(verbose_name='Подписка', default=False)

    def __str__(self):
        return self.username
