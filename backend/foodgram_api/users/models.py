from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель, описывающая пользователя"""

    username = models.CharField(
        verbose_name="Имя пользователя", max_length=256, unique=True
    )
    email = models.EmailField(
        verbose_name="Электронная почта", max_length=256, unique=True
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=256, unique=True, blank=True, null=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=256, unique=True, blank=True, null=True
    )
    is_subscribed = models.BooleanField(
        verbose_name="Подписка", default=False, blank=True, null=True
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Follow(models.Model):
    """Модель для работы c подписками"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following", verbose_name="Блогер"
    )

    def __str__(self):
        return f"{self.user} подписан на {self.following}"

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("user", "following"), name="unique_follow"),
        )

    class Meta:
        verbose_name = "Подписки"
        verbose_name_plural = verbose_name
