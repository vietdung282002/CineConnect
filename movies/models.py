from django.db import models
from genres.models import Genre
# Create your models here.
class Movie(models.Model):
    id = models.IntegerField(primary_key=True,null=False,blank=False)
    adult = models.BooleanField(null=False,blank=False)
    backdrop_path = models.ImageField(upload_to='pictures',null=True)
    budget = models.BigIntegerField (default=0)
    homepage = models.CharField(null=True,blank=True,max_length=200)
    original_language = models.CharField(max_length=10)
    original_title = models.CharField(max_length=200)
    overview = models.CharField(max_length=1000)
    poster_path = models.ImageField(upload_to='pictures',null=True)
    release_date = models.DateField(null=True,blank=True,)
    revenue = models.BigIntegerField (default=0)
    runtime = models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=50)
    tagline = models.CharField(null=True,blank=True,max_length=100)
    title = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre,related_name='movies')
    
    def __str__(self):
        return self.title
    