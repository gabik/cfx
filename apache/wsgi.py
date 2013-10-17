import os
import sys

sys.path.append('/home/gabi/cofix')
os.environ['DJANGO_SETTINGS_MODULE'] = 'cofix.settings'

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


