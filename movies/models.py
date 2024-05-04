from django.db import models
from genres.models import Genre
from people.models import Person
# Create your models here.
class Movie(models.Model):
    id = models.IntegerField(primary_key=True,null=False,blank=False)
    adult = models.BooleanField(null=False,blank=False)
    backdrop_path = models.CharField(null=True)
    budget = models.BigIntegerField (default=0)
    homepage = models.CharField(null=True,blank=True,max_length=200)
    original_language = models.CharField(max_length=10)
    original_title = models.CharField(max_length=200)
    overview = models.CharField(max_length=1000)
    poster_path = models.CharField(null=True)
    release_date = models.DateField(null=True,blank=True,)
    revenue = models.BigIntegerField (default=0)
    runtime = models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=50)
    tagline = models.CharField(null=True,blank=True,max_length=100)
    title = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre,related_name='movies')
    casts = models.ManyToManyField(Person,related_name='cast_movies', through="Cast")
    directors = models.ManyToManyField(Person,related_name='director_movies', through="Director")
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-release_date',)
    
class Cast(models.Model):
    id = models.AutoField(primary_key=True,null=False,blank=False)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='cast')
    cast = models.ForeignKey(Person,on_delete=models.CASCADE,related_name='person')
    charactor = models.CharField(max_length=200,null=True,blank=True,default='')
    order = models.IntegerField(null=True)
    
    def __str__(self):
        return self.cast.name + " ("+ self.movie.title + ")"
    
    class Meta:
        ordering = ('order',)
    
class Director(models.Model):
    id = models.AutoField(primary_key=True,null=False,blank=False)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='director')
    director = models.ForeignKey(Person,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.director.name + " ("+ self.movie.title + ")"
    
    