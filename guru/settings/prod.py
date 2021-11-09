from decouple import config

EMAIL_HOST= "smtp.gmail.com"
EMAIL_HOST_USER= config('EMAIL')
EMAIL_HOST_PASSWORD= config('PASSWORD')
EMAIL_PORT= 587
EMAIL_USE_TLS= True
DEFAULT_FROM_EMAIL= config('EMAIL')
EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
ANYMAIL = {
    "MAILJET_API_KEY": config('MAILJET_API_KEY'),
    "MAILJET_SECRET_KEY": config('MAILJET_SECRET_KEY'),
}
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
SITE_NAME = 'https://guru-lms-8fgu5.ondigitalocean.app'
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
'CacheControl': 'max-age=10',
}
AWS_LOCATION = 'media'
AWS_QUERYSTRING_AUTH=True
DEFAULT_FILE_STORAGE = 'guru.storage_back.PublicMediaStorage'
SITE_NAME = 'https://guru-lms-8fgu5.ondigitalocean.app'
AWS_PRIVATE_MEDIA_LOCATION = 'private'
PRIVATE_FILE_STORAGE = 'guru.storage_back.PrivateMediaStorage'

AWS_PUBLIC_MEDIA_LOCATION ='public'
PUBLIC_FILE_STORAGE = 'guru.storage_back.PublicMediaStorage'

AWS_S3_REGION_NAME = 'ap-south-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ENDPOINT_URL = f'https://fra1.digitaloceanspaces.com'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':config('DBNAME'),
        'USER':config('USER'),
        'PASSWORD':config('DBPASS'),
        'PORT':config('DBPORT'),
        'HOST':config('DBHOST'),
    }
}