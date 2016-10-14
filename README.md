Wikomega
======
##Steps to install:
1. git clone source code
   * git clone https://github.com/wikomega/wikodemo.git
2. install virtual env
   * Linux: sudo apt-get install python-virtualenv
   * Mac: sudo easy_install virtualenv
3. start virtualenv
   * virtualenv venv
   * source venv/bin/activate
4. Install all packages
   * pip install -r requirements/dev.txt
5. start demo
   * run manager.py runserver

##Git manual
1. merge branch xxx to master:
   * git checkout master
   * git pull origin master
   * git merge xxx
   * git push origin master
2. merge master to branch xxx
   * git checkout xxx
   * git pull 
   * git merge origin master
   * git push xxx
   
##choose top query
perl included.pl <(cat query_sample.txt | awk -F "\|" '{if(NR<100000)print $2}') wikisqldb-stream-header.txt 

