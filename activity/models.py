from django.db import models
from movies.models import Movie
from users.models import CustomUser
# Create your models here.
class Activity(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    type = models.IntegerField(null=False,blank=False)
    #type 1: User rervieww
    #type 2: User liked movie
    #type 3: User Watched movie
    #type 4: User like review
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='activity_movie')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activity_user')
    time_stamp = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('time_stamp',)