sudo apt-get install python-software-properties python-setuptools curl python-dev libxml2 libxml2-dev libxslt1-dev
curl -O http://python-distribute.org/distribute_setup.py
sudo python distribute_setup.py
rm distribute_setup.py
curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
sudo python get-pip.py
rm get-pip.py
sudo pip install --upgrade tornado sockjs-tornado requests lxml python-dateutil pymongo pika pexpect pytz