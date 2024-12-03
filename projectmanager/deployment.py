import os
from urllib.parse import urlparse
from .settings import *

# Set debug mode based on environment variable
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Secret Key from environment variable
SECRET_KEY = os.environ.get('MY_SECRET_KEY')

# Allowed hosts and CSRF trusted origins
ALLOWED_HOSTS = [os.environ.get('WEBSITE_HOSTNAME', 'localhost')]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('WEBSITE_HOSTNAME', 'localhost')]

# Middleware configuration
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

# Static files configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Azure PostgreSQL connection string
connection_string = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING')
if not connection_string:
    raise ValueError("AZURE_POSTGRESQL_CONNECTIONSTRING environment variable is not set.")

# Parse the Azure PostgreSQL connection string
parsed_url = urlparse(connection_string)
parameters = {
    'dbname': parsed_url.path[1:],  # Remove the leading '/'
    'user': parsed_url.username,
    'password': parsed_url.password,
    'host': parsed_url.hostname,
    'port': parsed_url.port or 5432,  # Default to port 5432 if not provided
}

# Ensure database name does not exceed PostgreSQL's 63-character limit
if len(parameters['dbname']) > 63:
    raise ValueError(f"Database name '{parameters['dbname']}' exceeds PostgreSQL's 63-character limit.")

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': parameters['dbname'],
        'USER': parameters['user'],
        'PASSWORD': parameters['password'],
        'HOST': parameters['host'],
        'PORT': parameters['port'],
        'OPTIONS': {
            'sslmode': 'require',  # Enforce SSL for secure connections
        },
    }
}

# Email backend configuration (optional, if sending emails)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.sendgrid.net')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'apikey')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Logging configuration for better visibility of errors during deployment
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
