from urllib.parse import urlencode

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme


class KeycloakAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        next_url = request.GET.get("next") or request.POST.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url, allowed_hosts={request.get_host()}
        ):
            return next_url
        return settings.LOGIN_REDIRECT_URL


class KeycloakSocialAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.email = data.get("email") or user.email
        user.first_name = data.get("given_name") or user.first_name
        user.last_name = data.get("family_name") or user.last_name

        is_superuser = self._is_superuser(sociallogin)
        User.objects.filter(email=user.email).update(
            first_name=user.first_name,
            last_name=user.last_name,
            is_superuser=is_superuser,
            is_staff=True,
        )
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.is_staff = True
        user.is_superuser = self._is_superuser(sociallogin)
        user.save()
        return user

    def _is_superuser(self, sociallogin) -> bool:
        userinfo = (sociallogin.account.extra_data or {}).get("userinfo", {})
        realm_roles = (userinfo.get("realm_access", {}) or {}).get("roles", [])
        return settings.PINCAMP_OIDC_ADMIN_ROLE in realm_roles


def oidc_logout_start(request):
    url = f"{settings.PINCAMP_OIDC_REALM_URL}/protocol/openid-connect/logout"
    params = {
        "client_id": settings.PINCAMP_OIDC_CLIENT_ID,
        "post_logout_redirect_uri": request.build_absolute_uri(
            "/admin/oidc/logout/complete/"
        ),
    }

    return redirect(f"{url}?{urlencode(params)}")


def oidc_logout_complete(request):
    logout(request)
    return redirect("/admin/")
