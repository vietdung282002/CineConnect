from django.db import models


# Create your models here.
class Person(models.Model):
    genre_options = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    )

    id = models.AutoField(primary_key=True, null=False, blank=False)
    adult = models.BooleanField(null=False, blank=False, default=False)
    biography = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    deathday = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=genre_options,
        default='others',
        null=False,
        blank=False
    )
    homepage = models.TextField(null=True, blank=True)
    known_for_department = models.CharField(null=True, max_length=50)
    name = models.CharField(max_length=200)
    place_of_birth = models.CharField(null=True, max_length=200)
    profile_path = models.CharField(default='default.jpg')

    def __str__(self):
        return self.name + " (" + str(self.id) + ")"
