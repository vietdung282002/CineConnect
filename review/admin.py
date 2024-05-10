from django.contrib import admin
from .models import Review,Reaction,Comment
# Register your models here.
admin.site.register(Review)
admin.site.register(Reaction)
admin.site.register(Comment)
