from django.contrib import admin
from .models import TfidfMatrixModel,MovieRecommend,CosineModel
# Register your models here.
admin.site.register(TfidfMatrixModel)
admin.site.register(MovieRecommend)
admin.site.register(CosineModel)
