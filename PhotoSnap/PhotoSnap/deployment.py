import os
from .settings import *
from .settings import BASE_DIR

SECRET_KEY = os.environ['SECRET']
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ['WEBSITE_HOSTNAME']]
DEBUG = False

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = ('whitenoise.storage.CompressedManifestStaticFilesStorage')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
connection_string = os.environ['AZURE_MYSQL_CONNECTION_STRING']
parameters = {pair.split('='):pair.split('=')[1] for pair in connection_string.split(' ')}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': connection_string('dbname'),
        'USER': connection_string('host'),
        'PASSWORD': connection_string('user'),
        'HOST': connection_string('password'),  
    }
}