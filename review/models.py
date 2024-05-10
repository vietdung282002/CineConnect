from django.db import models
from movies.models import Movie
from users.models import CustomUser

# Create your models here.
class Review(models.Model):
    id = models.AutoField(primary_key=True, null = False, blank=False)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='movie_review')
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_review')
    time_stamp = models.DateTimeField(auto_now=True)
    content = models.TextField(null=False, blank=False)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'], name='unique_movie_user_review'
            )
        ]
        ordering = ('time_stamp',)
        
    def __str__(self):
        return self.movie.title + " (" + self.user.username +")" 
    
class Reaction(models.Model):
    id = models.AutoField(primary_key=True, null = False, blank=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_like_review')
    review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name='related_review')
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True, null = False, blank=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_comment_review')
    review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name='comment_related_review')
    time_stamp = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=False, blank=False)
    
    class Meta:
        ordering = ('time_stamp',)