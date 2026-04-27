from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from image.views import health, image_list
from place_pictures.auth import oidc_logout_complete, oidc_logout_start


urlpatterns = [
    path("health", health, name="health"),
    path("admin/logout/", lambda _: redirect("/admin/oidc/logout/", permanent=False)),
    path("admin/oidc/logout/", oidc_logout_start),
    path("admin/oidc/logout/complete/", oidc_logout_complete),
    path("admin/", admin.site.urls),
    path("accounts/login/", lambda _: redirect("/admin/login/", permanent=False)),
    path("accounts/", include("allauth.urls")),
    path("", image_list, name="image-list"),
]
