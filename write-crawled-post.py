import sys

from collections import defaultdict
from utils import id_generator,utcnow
"""
    pid = db.Column(db.String(64), unique=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.username'))
    stream_id = db.Column(db.Integer, db.ForeignKey('streams.eid'))
"""

sys.stdout.write('Post\tpid\ttitle\tbody\tbody_html\ttimestamp\tauthor_id\tstream_id\n')

entitymap = defaultdict(set)

with open(sys.argv[1]) as infile:
    for line in infile:
       fields = line.strip('\r\t\n').split('\t')
       if len(fields)<2: continue
       caption = fields[1]
       eid = fields[0]
       entitymap[caption].add(eid)

with open(sys.argv[2]) as infile2:
    for line in infile2:
#        print line
        fields = line.strip('\r\t\n').split('\t')
        if fields[0] not in entitymap: continue
        for stream in entitymap[fields[0]]:
            pid = 'post-' + id_generator()
            title = fields[1]
            html = fields[2]
            author = 'wikomega'
            streamid = stream
            timestamp = str(utcnow())
            sys.stdout.write('%s\n' % '\t'.join([pid, title, html, author, streamid, timestamp]))
        
