from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class CustomUser(AbstractUser):
    options = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    )
    email = models.EmailField(unique=True)
    gender = models.CharField(
        max_length=20,
        choices=options,
        default='others',
        null=False,
        blank=False
    )
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.TextField(default='/default.jpg')

    def __str__(self):
        return self.username + " " + str(self.id)

    class Meta:
        ordering = ('id',)

class UpdatePasswordToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_passcode")
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() <= self.created_at + timedelta(minutes=15)