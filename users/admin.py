from django.contrib import admin
from .models import CustomUser
from users.models import Watched

# Register your models here.
admin.site.register(CustomUser)
admin.register(Watched)