from django.db import models

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
        ordering = ('-time_stamp',)

    def __str__(self):
        return self.movie.title + " (" + self.user.username + ")"


class Reaction(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_like_review')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='related_review')
    like = models.BooleanField(default=False)

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
