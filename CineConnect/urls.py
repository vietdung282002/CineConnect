"""
URL configuration for CineConnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('authentication/', include('users.urls')),
    path('user/', include('user_profile.urls')),
    path('genre/', include('genres.urls')),
    path('movie/', include('movies.urls')),
    path('person/', include('people.urls')),
    path('watched/', include('watched.urls')),
    path('favourite/', include('favourite.urls')),
    path('rate/', include('rating.urls')),
    path('review/', include('review.urls')),
    path('follow/',include('follow.urls')),
    path('test/',include('testwebjob.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI:

    path('doc', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI:

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
