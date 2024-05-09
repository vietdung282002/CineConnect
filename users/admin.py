from django.contrib import admin

from watched.models import Watched
from .models import CustomUser
from favourite.models import Favourite

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Watched)
admin.site.register(Favourite)