import os
from urllib.parse import urlparse

from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
DEBUG = True
SECRET_KEY = os.environ['MY_SECRET_KEY']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.RoleRequiredMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Handle connection string parsing
connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']

# If using URI format (postgresql://user:password@host/dbname)
if connection_string.startswith('postgresql://'):
    parsed_url = urlparse(connection_string)
    parameters = {
        'dbname': parsed_url.path[1:],  # Remove the leading '/'
        'user': parsed_url.username,
        'password': parsed_url.password,
        'host': parsed_url.hostname,
    }
else:
    # For key=value format (e.g., dbname=mydb user=myuser password=mypassword host=myhost)
    parameters = {pair.split('=')[0]: pair.split('=')[1] for pair in connection_string.split(' ')}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': parameters['dbname'],
        'USER': parameters['user'],
        'PASSWORD': parameters['password'],
        'HOST': parameters['host'],
    }
}
