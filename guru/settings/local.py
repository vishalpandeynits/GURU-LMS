import os
from pathlib import Path
from decouple import config, UndefinedValueError

SITE_ID = config('SITE_ID_LOCAL')
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_NAME = config('SITE_NAME')
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
}
}

try:
    SESSION_REDIS = {
        'host': config('REDIS_SERVER_HOST'),
        'port': config('REDIS_SERVER_PORT'),
        'db': 0, # TODO: Add multiple databases later for master, slave configuration
        'password': config('REDIS_SERVER_PASSWORD'),
        'prefix': 'session',
        'socket_timeout': 1,
        'retry_on_timeout': False,
    }
except UndefinedValueError:
    # No password
    SESSION_REDIS = {
        'host': config('REDIS_SERVER_HOST'),
        'port': config('REDIS_SERVER_PORT'),
        'db': 0, # TODO: Add multiple databases later for master, slave configuration
        'prefix': 'session',
        'socket_timeout': 1,
        'retry_on_timeout': False,
    }
SESSION_COOKIE_AGE = int(float(config('SESSION_TIMEOUT_HOURS')) * 60 * 60)


try:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                    "hosts": [("redis://:" + config('REDIS_SERVER_PASSWORD') + "@" + config('REDIS_SERVER_HOST') + ":" + config('REDIS_SERVER_PORT'))],
                    "capacity": 500,
                    "expiry": 40,
            },
        },
    }
except UndefinedValueError:
    # No password set
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [(config('REDIS_SERVER_HOST'), config('REDIS_SERVER_PORT'))],
                "capacity": 500,
                "expiry": 40,
            },
        },
    }


# Redis Server Settings
try:
    REDIS_SERVER_PASSWORD = config('REDIS_SERVER_PASSWORD')
except UndefinedValueError:
    REDIS_SERVER_PASSWORD = None


# # Cache Settings
# if REDIS_SERVER_PASSWORD:
#     CACHES = {
#         'default': {
#             'BACKEND': 'redis_cache.RedisCache',
#             'LOCATION': [
#                 f"{config('REDIS_SERVER_HOST')}: {config('REDIS_SERVER_PORT')}",
#             ],
#             'OPTIONS': {
#                 'DB': 1,
#                 'PASSWORD': config('REDIS_SERVER_PASSWORD'),
#                 'PARSER_CLASS': 'redis.connection.HiredisParser',
#                 'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
#                 'CONNECTION_POOL_CLASS_KWARGS': {
#                     'max_connections': 50,
#                     'timeout': 20,
#                 },
#                 'MAX_CONNECTIONS': 1000,
#                 'SERIALIZER_CLASS': 'redis_cache.serializers.JSONSerializer',
#                 'PICKLE_VERSION': -1,
#             },
#             'TIMEOUT': 60 * 60 * 24, # Items in the cache will expire after 1 day
#         },
#     }
# else:
#     CACHES = {
#         'default': {
#             'BACKEND': 'redis_cache.RedisCache',
#             'LOCATION': [
#                 f"{config('REDIS_SERVER_HOST')}: {config('REDIS_SERVER_PORT')}",
#             ],
#             'OPTIONS': {
#                 #'DB': 1,
#                 'PARSER_CLASS': 'redis.connection.HiredisParser',
#                 'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
#                 'CONNECTION_POOL_CLASS_KWARGS': {
#                     'max_connections': 50,
#                     'timeout': 20,
#                 },
#                 'MAX_CONNECTIONS': 1000,
#                 'SERIALIZER_CLASS': 'redis_cache.serializers.JSONSerializer',
#                 'PICKLE_VERSION': -1,
#             },
#             'TIMEOUT': 60 * 60 * 24, # Items in the cache will expire after 1 day
#         },
#     }

USE_CELERY=False
CELERY_BROKER_URL = 'redis://{}:{}'.format(config('REDIS_SERVER_HOST'), config('REDIS_SERVER_PORT'))
CELERY_RESULT_BACKEND = 'redis://{}:{}'.format(config('REDIS_SERVER_HOST'), config('REDIS_SERVER_PORT'))
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
