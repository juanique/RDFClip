start_dir=`pwd`
temp_dir=/tmp/rdfadmin

yes | sudo apt-get install python-beautifulsoup python-mechanize python-setuptools python-rdflib

sudo rm -rf $temp_dir
mkdir $temp_dir
cd $temp_dir
echo "Downloading Django 1.3. Please wait..."
wget http://www.djangoproject.com/download/1.3/tarball/ -O ./django.tar.gz -o /dev/null
echo "Downloaded. Uncompresing..."
tar xzvf django.tar.gz > /dev/null
cd Django-1.3
echo "Done. Installing..."
sudo python setup.py install > /dev/null
echo ""

#pistons
cd $temp_dir
echo "Downloading Django-Pistons. Please wait..."
wget http://www.djangoproject.com/download/1.3/tarball/ -O ./django.tar.gz -o /dev/null
wget http://bitbucket.org/jespern/django-piston/downloads/django-piston-0.2.2.tar.gz -o /dev/null
echo "Downloaded. Uncompresing..."
tar -xvzf django-piston-0.2.2.tar.gz > /dev/null
cd django-piston
echo "Done. Installing..."
sudo python setup.py install > /dev/null

#cleanup
sudo rm -rf $temp_dir
cd $start_dir
