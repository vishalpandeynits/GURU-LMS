import os
from pathlib import Path
from decouple import config

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