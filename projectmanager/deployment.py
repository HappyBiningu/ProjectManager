
import os
from urllib.parse import urlparse

from .settings import *
from .settings import BASE_DIR

# Read environment variables
ALLOWED_HOSTS = [os.environ.get('WEBSITE_HOSTNAME', 'localhost')]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('WEBSITE_HOSTNAME', 'localhost')]
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.environ.get('MY_SECRET_KEY')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files
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

# Azure PostgreSQL connection string
connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']

# Parse connection string
parsed_url = urlparse(connection_string)
parameters = {
    'dbname': parsed_url.path[1:],  # Remove leading '/'
    'user': parsed_url.username,
    'password': parsed_url.password,
    'host': parsed_url.hostname,
    'port': parsed_url.port or 5432,  # Use default port if not specified
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': parameters['dbname'],
        'USER': parameters['user'],
        'PASSWORD': parameters['password'],
        'HOST': parameters['host'],
        'PORT': parameters['port'],
        'OPTIONS': {
            'sslmode': 'require',  # Enforce SSL
        },
    }
}
