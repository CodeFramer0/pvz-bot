import logging
import sys
from datetime import timedelta
from pathlib import Path

from environs import Env

# ==================================================
# INITIALIZATION
# ==================================================
env = Env()
env.read_env()


# ==================================================
# LOGGING
# ==================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} - {name} - {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "[{levelname}] {name} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "robot": {  # Ваше приложение
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================
# CORE SETTINGS
# ==================================================
SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", True)

BOT_TOKEN = env.str("BOT_TOKEN")
PROTOCOL = env.str("PROTOCOL", "http")

ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==================================================
# APPS DEFINITION
# ==================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    # Third-party
    "rest_framework_simplejwt",
    "csp",
    "corsheaders",
    "rest_framework",
    "django_filters",
    "django_celery_beat",
    "django_celery_results",
    "drf_spectacular",
    "django_prometheus",
    # Local Apps
    "robot",
    "django_cleanup.apps.CleanupConfig",
]

# ==================================================
# MIDDLEWARE
# ==================================================
MIDDLEWARE = [
    "csp.middleware.CSPMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

# ==================================================
# DATABASE & CACHE
# ==================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": "pvz-db",
        "PORT": env.int("DB_PORT", 5432),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://pvz-redis:6379/1",
    }
}

# ==================================================
# STATIC & MEDIA (MinIO S3)
# ==================================================
MINIO_ENDPOINT = "http://minio:9000"
MINIO_DOMAIN = env.str("MINIO_DOMAIN")

MEDIA_URL = f"{PROTOCOL}://media.{MINIO_DOMAIN}/"
STATIC_URL = f"{PROTOCOL}://static.{MINIO_DOMAIN}/"

STORAGES = {
    "default": {
        "BACKEND": "core.storages_backends.MediaStorage",
        "OPTIONS": {
            "endpoint_url": MINIO_ENDPOINT,
            "access_key": env.str("MINIO_ROOT_USER"),
            "secret_key": env.str("MINIO_ROOT_PASSWORD"),
            "bucket_name": "media",
            "custom_domain": f"media.{MINIO_DOMAIN}",
            "querystring_auth": True,
        },
    },
    "staticfiles": {
        "BACKEND": "core.storages_backends.StaticStorage",
        "OPTIONS": {
            "endpoint_url": MINIO_ENDPOINT,
            "access_key": env.str("MINIO_ROOT_USER"),
            "secret_key": env.str("MINIO_ROOT_PASSWORD"),
            "bucket_name": "static",
            "custom_domain": f"static.{MINIO_DOMAIN}",
            "querystring_auth": False,
        },
    },
}

# ==================================================
# SECURITY / CSP / CORS
# ==================================================
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://pvz.localhost",
    f"http://{MINIO_DOMAIN}",
]

# Swagger UI CDN от Swagger (unpkg)
SWAGGER_CDN = "https://unpkg.com/swagger-ui-dist@4"
REDOC_CDN = "https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": [
            "'self'",
            "'unsafe-inline'",
            "'unsafe-eval'",
            "https://unpkg.com",  # Swagger UI
            "https://cdn.jsdelivr.net",  # ReDoc
            "https://fonts.googleapis.com",
            f"static.{MINIO_DOMAIN}",
        ],
        "style-src": [
            "'self'",
            "'unsafe-inline'",
            "https://unpkg.com",  # Swagger UI styles
            f"static.{MINIO_DOMAIN}",
            "https://fonts.googleapis.com",
        ],
        "img-src": [
            "'self'",
            "data:",
            "https://unpkg.com",
            "https://fonts.googleapis.com",
            f"media.{MINIO_DOMAIN}",
            f"static.{MINIO_DOMAIN}",
        ],
        "font-src": [
            "'self'",
            "https://unpkg.com",
            "https://fonts.googleapis.com",
            f"static.{MINIO_DOMAIN}",
        ],
        "connect-src": [
            "'self'",
            "pvz.localhost",
            "https://unpkg.com",
            "https://fonts.googleapis.com",
            "https://cdn.jsdelivr.net",
            f"static.{MINIO_DOMAIN}",
        ],
        "frame-src": ["'self'"],
    }
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# ==================================================
# TEMPLATES & I18N
# ==================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Asia/Yekaterinburg"
USE_I18N = True
USE_TZ = True

# ==================================================
# CELERY
# ==================================================
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

# ==================================================
# REST FRAMEWORK
# ==================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# ==================================================
# JWT CONFIGURATION
# ==================================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
}

# ==================================================
# AUTH
# ==================================================
AUTH_USER_MODEL = "robot.AppUser"
LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/admin/"

# ==================================================
# DRF SPECTACULAR (Swagger/OpenAPI)
# ==================================================
SPECTACULAR_SETTINGS = {
    "TITLE": "PVZ Bot API",
    "DESCRIPTION": "API для управления пунктами выдачи",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,

    # Swagger UI
    "SWAGGER_UI_DIST": "https://unpkg.com/swagger-ui-dist@4",
    "SWAGGER_UI_FAVICON_URL": "https://unpkg.com/swagger-ui-dist@4/favicon-32x32.png",
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,  # ← сохраняет токен между перезагрузками Swagger
        "displayOperationId": True,
        "filter": True,
        "showExtensions": True,
        "deepLinking": True,
        "defaultModelsExpandDepth": 1,
        "docExpansion": "list",
        "tryItOutEnabled": True,
    },

    # ReDoc
    "REDOC_DIST": "https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js",

    # SECURITY - добавляет кнопку AUTHORIZE
    "SECURITY": [{"bearerAuth": []}],
    "COMPONENTS": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT Authorization header using Bearer token",
            }
        }
    },
}
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Эти настройки можно оставить, хоть они не используются
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = "noreply@pvz.localhost"
