from django.db import models

from movies.models import Movie
from users.models import CustomUser


class Favourite(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favourite_movie')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favourite_list')
    time_stamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user.id) + " ( " + self.movie.title + ")"

    class Meta:
        ordering = ('time_stamp',)

# Create your models here.
