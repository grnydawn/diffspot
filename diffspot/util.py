# -*- coding: utf-8 -*-

import os
import time
import datetime
import hashlib


def longSHA(msg):
    return hashlib.sha1(msg).hexdigest()

def shortSHA(msg):
    return longSHA(msg)[:8]


def datetimestr():
    ts = time.time()
    utc = datetime.datetime.utcfromtimestamp(ts)
    now = datetime.datetime.fromtimestamp(ts)
    tzdiff = now - utc
    secdiff = int(tzdiff.days*24*3600 + tzdiff.seconds)
    tzstr = '{0}{1}'.format('+' if secdiff>=0 else '-',
        time.strftime('%H:%M:%S', time.gmtime(abs(secdiff))))
    return '{0} {1}'.format(str(now), tzstr)


def cdrepo(cwd=None):

    if cwd is None:
        cwd = os.getcwd()
    else:
        cwd = os.path.abspath(cwd)
 
    while(cwd):
        if os.path.exists(os.path.join(cwd, '.git')):
            return cwd
        cwd, _ = os.path.split(cwd)
