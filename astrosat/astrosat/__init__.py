from .celery import app as celery_app
import os
import sys

###########################
# what is the app called? #
###########################

APP_LABEL = "astrosat"

#########################
# setup the task broker #
#########################

__all__ = ['celery_app']

####################################
# what version is the app/project? #
####################################

__version_info__ = {
    'major': 1,
    'minor': 0,
    'patch': 0,
}


def get_version():
    version = ".".join(str(value) for value in __version_info__.values())
    return version


__version__ = get_version()


##############################################
# control django via a module                #
# (makes it easier to install w/ setuptools) #
##############################################

def manage_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "astrosat.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
