"""
Django settings for contato_django project.
"""

from pathlib import Path
import os

# ==============================
# Caminho base do projeto
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# Configurações básicas
# ==============================
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-zh+(9be-2gtjd!(_97+w=0nxsi%)udfh&l-_3zch3vf-0ux4dg"  # fallback para dev
)

DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = (
    ["*"] if DEBUG else os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
)

# ==============================
# Aplicativos instalados
# ==============================
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # App do projeto
    "contato",

    # Terceiros
    "rest_framework",
    "django_filters",
    "rest_framework.authtoken",
]

# ==============================
# Middleware
# ==============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==============================
# URLs e WSGI
# ==============================
ROOT_URLCONF = "contato_django.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # diretório global de templates
        "APP_DIRS": True,  # procura automaticamente em cada app/templates
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "contato_django.wsgi.application"

# ==============================
# Banco de dados
# ==============================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==============================
# Validação de senha
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================
# Internacionalização
# ==============================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ==============================
# Arquivos estáticos (CSS, JS, imagens)
# ==============================
STATIC_URL = "/static/"

# Ajustado para usar a pasta contato/static/
STATICFILES_DIRS = [
    BASE_DIR / "contato" / "static"
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# ==============================
# Arquivos de mídia (uploads de usuários)
# ==============================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==============================
# Configurações padrão
# ==============================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================
# Configurações do DRF
# ==============================
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,

    # 🔑 Autenticação e Permissões
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
