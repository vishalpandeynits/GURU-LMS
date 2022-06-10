from pathlib import Path
import os
from decouple import config
from .local import *

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
SECRET_KEY = config('SECRET')
ALLOWED_HOSTS = ['*']
DEBUG = config('DEBUG', default=False, cast=bool)

INBUILT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_comments',
    'rest_framework',
    'crispy_forms',
    "django_filters",
    'storages',
    'imagekit',
    'notifications',
    'django_quill',
]

GURU_APPS = [
    'apps.assignment',
    'apps.announcement',
    'apps.basic',
    'apps.classroom',
    'apps.subject',
    'apps.users',
    'apps.poll',
    'apps.resource'
]

INSTALLED_APPS = INBUILT_APPS + THIRD_PARTY_APPS + GURU_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'guru.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS' : True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                "apps.context_preprocess.data",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guru.emaillogin.EmailBackend',
)

WSGI_APPLICATION = 'guru.wsgi.application'

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True 

DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}

QUILL_CONFIGS = {
    'default':{
        'theme': 'snow',
        'modules': {
            'syntax': True,
            'toolbar': [
                [
                    {'font': []},
                    { 'size': ['small', 'large', 'huge'] },
                    {'header': []},
                    {'align': []},
                    {'image':[]},
                    
                    'bold', 'italic', 'underline', 'strike','link','blockquote','code-block',
                    {'color': []},
                    {'background': []},
                    { 'list': 'ordered'}, { 'list': 'bullet' },
                ]
            ]
        },
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
  BASE_DIR/"static",
)

LOGIN_REDIRECT_URL ='/classroom/homepage/'
LOGOUT_REDIRECT_URL = '/'

#all-auth registraion settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_UNIQUE_EMAIL=True
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_USERNAME_REQUIRED =False
ACCOUNT_USERNAME_VALIDATORS = None

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [ 
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SOCIALACCOUNT_QUERY_EMAIL=ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_EMAIL_REQUIRED=ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_STORE_TOKENS=False

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}