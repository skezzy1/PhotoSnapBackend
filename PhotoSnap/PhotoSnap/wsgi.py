import os
from django.core.wsgi import get_wsgi_application

setting_module =  'PhotoSnap.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'PhotoSnap.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)

application = get_wsgi_application()
