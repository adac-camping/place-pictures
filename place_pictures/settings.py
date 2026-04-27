import os
import re
from distutils.util import strtobool
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
DEBUG = bool(strtobool(os.getenv("DEBUG", "False")))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.openid_connect",
    "image",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ROOT_URLCONF = "place_pictures.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "place_pictures.wsgi.application"
ASGI_APPLICATION = "place_pictures.asgi.application"

PINCAMP_OIDC_CLIENT_ID = os.getenv("PINCAMP_OIDC_CLIENT_ID", "")
PINCAMP_OIDC_CLIENT_SECRET = os.getenv("PINCAMP_OIDC_CLIENT_SECRET", "")
PINCAMP_OIDC_REALM_URL = os.getenv("PINCAMP_OIDC_REALM_URL", "")
PINCAMP_OIDC_ADMIN_ROLE = os.getenv("PINCAMP_OIDC_ADMIN_ROLE", "admin")
PINCAMP_OIDC_DISCOVERY_URL = (
    f"{PINCAMP_OIDC_REALM_URL}/.well-known/openid-configuration"
    if PINCAMP_OIDC_REALM_URL
    else ""
)

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_PROVIDERS = {
    "openid_connect": {
        "OAUTH_PKCE_ENABLED": True,
        "APP": {
            "provider_id": "keycloak",
            "name": "Login with PiNCAMP Keycloak",
            "client_id": PINCAMP_OIDC_CLIENT_ID,
            "secret": PINCAMP_OIDC_CLIENT_SECRET,
            "settings": {
                "server_url": PINCAMP_OIDC_DISCOVERY_URL,
                "fetch_userinfo": True,
            },
        },
    }
}

ACCOUNT_ADAPTER = "place_pictures.auth.KeycloakAccountAdapter"
SOCIALACCOUNT_ADAPTER = "place_pictures.auth.KeycloakSocialAdapter"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DEBUG else "https"
LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "/admin/"

connection_string = os.getenv("DB_CONNECTION_STRING")
if connection_string:
    db_settings = (
        re.compile(
            r"^(?P<engine>[^:]+)://(?P<user>[^:]+):(?P<password>[^@]+)"
            r"@(?P<host>[^\/:]+):(?P<port>\d+)/(?P<name>.*)$"
        )
        .search(connection_string)
        .groupdict()
    )
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": db_settings["name"],
            "USER": db_settings["user"],
            "PASSWORD": db_settings["password"],
            "HOST": db_settings["host"],
            "PORT": db_settings["port"],
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ALLOWED_HOSTS = ["*"]
