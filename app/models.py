from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator as MIN
from django.core.validators import MaxValueValidator as MAX
from django.db.models import PositiveSmallIntegerField as PSIField
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError as RestValidationError


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    student = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    @property
    def is_student(self):
        return self.student


class Question(models.Model):
    FORMAT_CHOICES = (
        (1, "NUMBER"),
        (2, "SMALL_TEXT"),
        (3, "LONG_TEXT"),
        (4, "SELECT_BOX"),
        (5, "RADIO_BUTTON"),
    )
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    format = PSIField(choices=FORMAT_CHOICES, validators=[MIN(1), MAX(5)])
    question = models.TextField()
    choice = models.JSONField()
    teacher_answer = models.TextField(null=True, blank=True)
    point = PSIField(_("PRIORITY"), default=3, validators=[MIN(1), MAX(5)])

    def save(self, *args, **kwargs):
        if self.format not in [1, 2, 3] and not self.choice:
            raise RestValidationError({"error": f"this question with format({self.format}) need choices"})
        super().save(*args, **kwargs)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    student_answer = models.TextField(null=True, blank=True)
    point = PSIField(_("PRIORITY"), default=3, validators=[MIN(1), MAX(5)])
    completed = models.BooleanField(default=False)
