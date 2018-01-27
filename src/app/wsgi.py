"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

os.environ.setdefault("django_secret",
                      ")(wwa_1t=uzs_fp3!pl+y(p1stoh+a1-md7!*$gtc4692cvu0q")
os.environ.setdefault("mediawiki_key", "d8ce05a433c07ca0899c691bb019eaa2")
os.environ.setdefault("mediawiki_secret",
                      "935a178a145ec703f3b44c2ddc0c787ba33db8d6")
os.environ.setdefault("mediawiki_callback",
                      "http://127.0.0.1:8080/oauth/complete/mediawiki/")

application = get_wsgi_application()
