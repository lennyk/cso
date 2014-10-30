import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cso.settings")

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
