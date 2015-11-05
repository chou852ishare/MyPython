# -*- coding: utf-8 -*-

import urllib2
import sys
import os
import re
reload(sys)
sys.setdefaultencoding('utf-8')


start = sys.argv[1]
end = sys.argv[2]
url = 'http://android.myapp.com/myapp/detail.htm?apkName=%s'
#ids = xrange(1049137, 2233259)
ids = xrange(int(start), int(end))


for id in ids:
    try:
        w = urllib2.urlopen(url % id, timeout=3)
        s = w.read().encode('utf-8', 'ignore')
        m = re.search(r'package=(.*?)">', s)
        fname = './html_list/%s.html' % (m.group(1)+'_'+str(id))
        if not os.path.exists(fname):
            with open(fname, 'w') as f:
                print >> f,s
    except:
        pass
