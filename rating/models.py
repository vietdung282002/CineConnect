from django.db import models
from movies.models import Movie
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Rating(models.Model):
    id = models.AutoField(primary_key=True, null = False, blank=False)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='movie_rating')
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_rating')
    rate = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'], name='unique_movie_user_rating'
            )
        ]
        ordering = ('rate',)
        
    def __str__(self):
        return self.movie.title + " (" + self.user.username + " " + str(self.rate) + ")"  