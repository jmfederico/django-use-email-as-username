"""Minimum settings to run tests."""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "7a%8!3)_=_c04_i@ai1yfw=fz&gf6(b5vp6(@_#h4&n9276vjj"

DEBUG = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django_use_email_as_username.apps.DjangoUseEmailAsUsernameConfig",
    "custom_user_test.apps.CustomUserTestConfig",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "tests.urls"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

USE_TZ = True

AUTH_USER_MODEL = "custom_user_test.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
