from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254, blank=False,
                              null=False)
    username = models.CharField(unique=True, max_length=150, blank=False,
                                null=False)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    password = models.CharField(max_length=150, blank=False, null=False)

    @property
    def is_admin(self):
        return self.is_superuser

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscriptions(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                               related_name='followee')

    class Meta:
        unique_together = ['user', 'author']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
