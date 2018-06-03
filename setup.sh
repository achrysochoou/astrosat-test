#!/bin/sh

INSTALL_DIR="astrosat-test-repository"
VIRTUAL_ENV="astrosat-test-env"

while getopts d:e: OPT
do
  case $OPT in
    d) INSTALL_DIR="$OPTARG";;
    v) VIRTUAL_ENV="$OPTARG";;
    *) echo $USAGE>&2;
       exit;;
  esac
done

git clone https://github.com/allynt/astrosat-test.git $INSTALL_DIR

#mkdir -p ~/.config
#cp $INSTALL_DIR/astrosat.conf.TEMPLATE ~/.config/astrosat.conf
sudo apt-get install -y erlang
sudo apt-get install rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV 

. $VIRTUAL_ENV/bin/activate

pip install rcssmin==1.0.6 --install-option="--without-c-extensions" 
pip install rjsmin==1.0.12 --install-option="--without-c-extensions" 
pip install $INSTALL_DIR/dist/astrosat-test*.tar.gz

astrosat-test migrate
astrosat-test loaddata $INSTALL_DIR/astrosat/astrosat/fixtures/sites.json
astrosat-test loaddata $INSTALL_DIR/astrosat/astrosat/fixtures/tasks.json
astrosat-test collectstatic --noinput
astrosat-test compress

echo "Hooray, you're done"
echo "now just active the virtual environment: '. $VIRTUAL_ENV/bin/activate'"
echo "make sure that the task broker is running: 'astrosat-test celery_worker'"
echo "run the django server: 'astrosat-test runserver'"
echo "and goto 'http://localhost:8000"


