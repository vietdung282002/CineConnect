from django.db import models
from datetime import datetime, timedelta,timezone
from movies.models import Movie
from users.models import CustomUser


# Create your models here.
class Review(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_review')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_review')
    time_stamp = models.DateTimeField(auto_now=True)
    content = models.TextField(null=False, blank=False)
    popular = models.FloatField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'], name='unique_movie_user_review'
            )
        ]
        ordering = ('popular','-time_stamp',)

    def __str__(self):
        return self.movie.title + " (" + self.user.username + ")"
    
    def update_popular(self):
        time_difference = datetime.now(timezone.utc) - self.time_stamp
        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        day_ago = datetime.now(timezone.utc) - timedelta(days=1)
        hours_difference = time_difference.total_seconds() / 3600  # Convert to hours

        # Constants
        reaction_count = Reaction.objects.filter(review=self,time_stamp__lt=day_ago).count()
        comment = Comment.objects.filter(review=self,time_stamp__lt=day_ago).count()
        gravity = 1.8
        if hours_difference > 0:
            self.score = (reaction_count + comment) / pow(hours_difference + 2, gravity)
        else:
            self.score = 0  # Default score if time difference is 0 (edge case)

        self.save()    
    
class Review_visit(models.Model):
    id = models.IntegerField(primary_key=True, null=False, blank=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='visit')
    time_stamp = models.DateTimeField(auto_now=True)

class Reaction(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_like_review')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='related_review')
    like = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now=True)
    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'review'], name='unique_reaction'
            )
        ]

    def __str__(self):
        return f'Reaction by {self.user.username}'


class Comment(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_comment_review')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comment_related_review')
    time_stamp = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ('time_stamp',)

    def __str__(self):
        return f'Comment by {self.user.username}'
