Wikomega
======
#Steps to install:
##git clone source code
###git clone https://github.com/wikomega/wikodemo.git
##install virtual env
###Linux: sudo apt-get install python-virtualenv
###Mac: sudo easy_install virtualenv
##start virtualenv
###virtualenv venv
###source venv/bin/activate
##Install all packages
###pip install -r requirements/dev.txt
##start demo
###run manager.py runserver


#choose top query
perl included.pl <(cat query_sample.txt | awk -F "\|" '{if(NR<100000)print $2}') wikisqldb-stream-header.txt 

