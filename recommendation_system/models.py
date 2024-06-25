from django.db import models
import pickle
from movies.models import Movie
from users.models import CustomUser
# Create your models here.
class TfidfMatrixModel(models.Model):
    data = models.BinaryField()

    def save_matrix(self, matrix):
        self.data = pickle.dumps(matrix)
        self.save()

    def get_matrix(self):
        return pickle.loads(self.data)

class CosineModel(models.Model):
    data = models.BinaryField()

    def save_matrix(self, matrix):
        self.data = pickle.dumps(matrix)
        self.save()

    def get_matrix(self):
        return pickle.loads(self.data)
    
class MovieRecommend(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="user")
    movie= models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='movie_recommend')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['movie', 'user'], name='unique_movie_recommend'
            )
        ]
        
    def __str__(self):
        return self.user.username + " (" + str(self.movie.title) + ")"

