import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

REQUIREMENTS = [
    # just did `pip freeze` to get this list...
    # ...doubt I need them all
    "amqp==2.3.2",
    "billiard==3.5.0.3",
    "celery==4.1.1",
    "certifi==2018.4.16",
    "chardet==3.0.4",
    "Django==2.0.5",
    "django-appconf==1.0.2",
    "django-celery-beat==1.1.1",
    "django-celery-results==1.0.1",
    "django-compressor==2.2",
    "django-crispy-forms==1.7.2",
    "django-filter==1.1.0",
    "djangorestframework==3.8.2",
    "idna==2.6",
    "kombu==4.2.1",
    "pytz==2018.4",
# these 2 packages are required by django-compressor
# but they have options (--without-c-extensions)
# and I don't know how to add those to setuptools
# so I do it in the install script prior to `pip install astrosat-test.tar.gz`
# oh well
#    "rcssmin==1.0.6",
#    "rjsmin==1.0.12",
    "requests==2.18.4",
    "urllib3==1.22",
    "vine==1.1.4",
]

NAME="astrosat-test"
VERSION="1.0.0"

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license='MIT License', 
    description='Astrosat Django Test',
    author='Allyn Treshansky',
    author_email="allyn.treshansky@gmail.com",
    entry_points={
        'console_scripts': [
            '{0}=astrosat:manage_django'.format(NAME)
        ]
    }
)

