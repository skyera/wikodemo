#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import sys
import codecs

from kitchen.text.converters import getwriter
from kitchen.text.converters import to_unicode, to_bytes

#UTF8Writer = getwriter('utf8')
#sys.stdout = UTF8Writer(sys.stdout)

for line in sys.stdin:
#    print line
    x = to_unicode(line)
#    x = line.encode('utf-8','replace')
    sys.stdout.write('%s' % to_bytes(x))
