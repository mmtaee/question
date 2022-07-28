from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    student = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    @property
    def is_student(self):
        return self.student


# "Authorization: Token TOKEN_RECIVED_FROM_BACKEND_AT_LOGIN"
