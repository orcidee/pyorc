"""
WSGI config for pyorc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from pyorc.config import get_project_root_path, import_env_vars

import_env_vars(os.path.join(get_project_root_path(), "envdir"))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "pyorc.config.settings.base"
)

application = get_wsgi_application()
