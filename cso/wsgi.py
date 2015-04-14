import os
from dj_static import Cling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cso.settings")

from configurations.wsgi import get_wsgi_application

application = Cling(get_wsgi_application())
