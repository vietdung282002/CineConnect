from django.contrib import admin
from .models import TfidfMatrixModel,MovieRecommend
# Register your models here.
admin.site.register(TfidfMatrixModel)
admin.site.register(MovieRecommend)