from pathlib import Path
from environs import Env

# ==================================================
# INITIALIZATION
# ==================================================
env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================
# CORE SETTINGS
# ==================================================
SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", True)

BOT_TOKEN = env.str("BOT_TOKEN")
PROTOCOL = env.str("PROTOCOL", "http")

ALLOWED_HOSTS = ["*"]  # На проде лучше заменить на конкретные домены

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
    
    # Third-party
    "csp",
    "corsheaders",
    "django_cleanup.apps.CleanupConfig",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "django_celery_beat",
    "django_celery_results",
    
    # Local Apps
    "robot",
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

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'", f"static.{MINIO_DOMAIN}"],
        "style-src": ["'self'", "'unsafe-inline'", f"static.{MINIO_DOMAIN}"],
        "img-src": ["'self'", "data:", f"media.{MINIO_DOMAIN}", f"static.{MINIO_DOMAIN}"],
        "font-src": ["'self'", f"static.{MINIO_DOMAIN}"],
        "connect-src": ["'self'", "pvz.localhost", "pvz.ru", f"static.{MINIO_DOMAIN}"],
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
# CELERY & REST FRAMEWORK
# ==================================================
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]


# ==================================================
# AUTH & LOGIN
# ==================================================
LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/admin/"
