import os

from django.core.wsgi import get_wsgi_application

settings_module = 'projectmanager.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'projectmanager.settings'

# Log the settings module and environment variable to debug
print(f"Using settings module: {settings_module}")
print(f"AZURE_POSTGRESQL_CONNECTIONSTRING: {os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')}")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
