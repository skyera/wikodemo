# Test by zhigang
import sys
import uuid,re, string
import datetime

def id_generator():
    return str(uuid.uuid4())

def utcnow():
    return datetime.datetime.utcnow()
            

def remove_punct(sent):
    regex = re.compile(r'([%s])' % re.escape(string.punctuation))
    sent = regex.sub(r' ', sent)
    sent = re.sub('\s+',' ',sent)
    sent = re.sub('\s+$','',sent)
    sent = re.sub('^\s+','',sent)
    return sent

def LOG(sent):
    sys.stdout.write('%s\n' % sent)
