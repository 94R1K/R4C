from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('robots.urls', namespace='robots')),
    path('admin/', admin.site.urls),
]
