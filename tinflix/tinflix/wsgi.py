"""
WSGI config for tinflix project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import sys
import os

from django.core.wsgi import get_wsgi_application

sys.path = ['/var/www/tinflix/tinflix/'] + sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tinflix.settings")
application = get_wsgi_application()
