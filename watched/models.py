from django.db import models

from movies.models import Movie
from users.models import CustomUser


class Watched(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='watched_list')
    time_stamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user.id) + " ( " + self.movie.title + ")"

    class Meta:
        ordering = ('time_stamp',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'], name='unique_movie_user_watched'
            )
        ]

