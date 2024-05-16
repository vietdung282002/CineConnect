from django.contrib.auth.models import AbstractUser
from django.db import models


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
    profile_pic = models.TextField(default='default.jpg')

    def __str__(self):
        return self.username + " " + str(self.id)

    class Meta:
        ordering = ('id',)
