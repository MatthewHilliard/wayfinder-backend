import os
from datetime import timedelta
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', default=False))

# SECURITY WARNING: update this when there is a production host
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# Define the custom user model
AUTH_USER_MODEL = 'wayfinder.User'

# Define the site id
SITE_ID = 1

# Define the server site URL
if DEBUG:
    WEBSITE_URL = 'http://localhost:8000'
else:
    WEBSITE_URL = 'https://wayfinder-backend-prod-aac06f5eb6d4.herokuapp.com'

# JWT object settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": SECRET_KEY,
    "ALGORITHM": "HS512",
}

# Authentication settings
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# REST framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# Only allow the following origins to access the API
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:3000",
    "https://wayfinder-backend-prod-aac06f5eb6d4.herokuapp.com",
    "https://wayfinder-frontend-prod-094351007f71.herokuapp.com"
]

CORS_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:3000",
    "https://wayfinder-backend-prod-aac06f5eb6d4.herokuapp.com",
    "https://wayfinder-frontend-prod-094351007f71.herokuapp.com"
]

CORS_ORIGINS_WHITELIST = [
    "http://localhost:8000",
    "http://localhost:3000",
    "https://wayfinder-backend-prod-aac06f5eb6d4.herokuapp.com",
    "https://wayfinder-frontend-prod-094351007f71.herokuapp.com"
]

# Django REST Auth settings
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": True
}

# Application definitions
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.sites',
    
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',  # Required to avoid ImproperlyConfigured error
    
    'dj_rest_auth',
    'dj_rest_auth.registration',
    
    'corsheaders',
    
    'cities_light',
    
    'wayfinder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'wayfinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('SQL_ENGINE', 'django.db.backends.postgresql'),
            'NAME': os.getenv('SQL_DATABASE', 'postgres'),
            'USER': os.getenv('SQL_USER', 'postgresuser'),
            'PASSWORD': os.getenv('SQL_PASSWORD', 'postgrespassword'),
            'HOST': os.getenv('SQL_HOST', 'localhost'),
            'PORT': os.getenv('SQL_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
