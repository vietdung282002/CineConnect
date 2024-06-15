from django.contrib import admin

from .models import CustomUser,UpdatePasswordToken

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UpdatePasswordToken)

