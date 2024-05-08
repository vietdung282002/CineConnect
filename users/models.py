from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie

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
        default = 'others',
        null=False,
        blank=False
        )
    bio=models.CharField(null=True,blank=True)
    profile_pic = models.ImageField(upload_to='pictures', default='default.jpg')
    watched = models.ManyToManyField(Movie,related_name='user_watched',through='Watched')

    def __str__(self):
        return self.username + " " + str(self.id)
    
    class Meta:
        ordering = ('id',)
    
class Watched(models.Model):
    id = models.AutoField(primary_key=True,null=False,blank=False)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='movie')
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='watched_list')
    
    def __str__(self) -> str:
        return str(self.user.id) + " ( " +self.movie.title+ ")"