from django.contrib import admin
from .models import Movie,Cast,Director
# Register your models here.
admin.site.register(Movie)
admin.site.register(Cast)
admin.site.register(Director)