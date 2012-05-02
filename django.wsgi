import os
import sys

sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['DJANGO_WSGI'] = 'True'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = os.path.realpath(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)
