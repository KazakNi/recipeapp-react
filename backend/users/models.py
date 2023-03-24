from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254, blank=False, null=False)
    username = models.CharField(unique=True, max_length=150, blank=False, null=False)
    first_name = models.CharField(max_length=150, blank=False, null=False) 
    last_name = models.CharField(max_length=150, blank=False, null=False)
    password = models.CharField(max_length=150, blank=False, null=False)
    staff = models.BooleanField(default=False)

    @property
    def is_staff(self):
        return self.staff

    def __str__(self):
        return self.username

class Subscription(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='followee')

    class Meta:
        unique_together = [ 'user', 'author']
