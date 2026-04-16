from django.contrib import admin
from django.urls import path

from image.views import image_list


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", image_list, name="image-list"),
]
