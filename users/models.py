from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    options = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others','Others')
    )
    email = models.EmailField(unique=True)
    gender = models.CharField(
        max_length = 20,
        choices = options,
        default = 'male',
        null=False,
        blank=False
        )
    bio=models.CharField(null=True,blank=True)
    profile_pic = models.ImageField(upload_to='pictures', default='default.jpg')

    def __str__(self):
        return self.username