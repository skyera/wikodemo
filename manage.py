#!/usr/bin/env python
import os,json,string
from flask import request,current_app
from collections import defaultdict
from app import create_app, db
from app.models import User, Role, Permission, Post, EntityStream, SearchKey
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask.ext.alchemydumps import AlchemyDumps, AlchemyDumpsCommand
from kitchen.text.converters import to_unicode, to_bytes

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)



def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission,
                Post=Post)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

alchemydumps = AlchemyDumps(app, db)
manager.add_command('alchemydumps', AlchemyDumpsCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


    
@manager.option("--file", help='database file name')
def import_db(file):
    dbfile = open(file)
    heads = dbfile.readline().strip('\r\t\n').split('\t')
    table=heads[0]
    schemas = heads[1:]
    for line in dbfile:
        fields = line.strip('\r\t\n').split('\t')
        if len(fields)==0 or fields[0]=='': continue
        options=defaultdict(str)
        for i in range(min(len(fields), len(heads)-1)):
            options[heads[i+1]] = fields[i]
        print options
        if table=='User':
            user = User.query.filter_by(username=options['username']).first()
            if user==None: user=User()
            entry = user.assign(**options)
            db.session.add(entry)
        elif table=='Post':
            post = Post.query.filter_by(pid=options['pid']).first()
            if post==None: post=Post()
            entry = post.assign(**options)  #unpack dictionary into keyword arguments
            db.session.add(entry)
        elif table=='EntityStream':
            entitystream = EntityStream.query.filter_by(eid=options['eid']).first()
            if entitystream == None: entitystream=EntityStream()
            entry = entitystream.assign(**options)
            if options['suggestion']: 
                for s in  options['suggestion'].split('|'):
                    searchkey = SearchKey.query.filter_by(word=s).first()
                    if searchkey == None: 
                        searchkey = SearchKey(s)
#                        print searchkey.word
                    entry.suggestion.append(searchkey)
            db.session.add(entry)
    db.session.commit()
    
@manager.command
def test_db():
  query='evergreen san jose'
  stream = EntityStream.query.filter_by(caption=query).first()
  print stream.eid, stream.creator, stream.id
  for sugg in stream.suggestion.all():
       print "sugg:", sugg.word, sugg.id
  query='evergreen'
  skey = SearchKey.query.filter_by(word=query).all()
  print skey
  for item in skey:
      print item
      print item.word
      print item.id
      for streams in item.streams.all():
          print streams.eid
  
@manager.command
def test_db_user():
    username='ruiqiang'
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    posts = pagination.items
    print user.id, user.username
    print user.posts.first().id
#    print posts
    
if __name__ == '__main__':
    manager.run()
