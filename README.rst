=============
astrosat-test
=============

astrosat-test is a simple Django project/app to prove to Astrosat that I can code in Django.

About
-----

This project gathers data from NASA about their facilities.
It does this via a periodic celery task that runs every 5 minutes.
Users can also update facility data via a button on the home page (if they don't feel like waiting 5 minutes).
Active facilities currently in the database can be viewed via a RESTful API endpoint.


Installation
------------

1. download and run `setup.sh <https://raw.githubusercontent.com/allynt/astrosat-test/master/setup.sh>`_

 - start the installed virtual environment
 - run celery in the background `astrosat-test celery_worker`
 - run the server `astrosat-test runserver`

2. but if that fails, clone the project from github and run it the normal Django way...

 -  make sure you have python3+
 -  make sure you have rabbitmq
 -  create a virtualenv
 -  install everything in requirements.txt to the virtualenv
 -  (note that "rcssmin" & "rjsmin" may need to be installed w/ the "--without-c-extensions" flag)
 -  run `python astrosat/manage.py migrate`
 -  run `python astrosat/manage.py createsuperuser`
 -  run `python astrosat/manage.py loaddata astrosat/astrosat/fixtures/sites.json`
 -  run `python astrosat/manage.py loaddata astrosat/astrosat/fixtures/tasks.json`
 -  run `python astrosat/manage.py collectstatic --noinput`
 -  run `python astrosat/manage.py compress`
 -  run `python astrosat/manage.py celery_worker`
 -  run `python astrosat/manage.py runserver`


3. Visit http://localhost:8000 and enjoy
