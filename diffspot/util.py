# -*- coding: utf-8 -*-

import hashlib


def longSHA(msg):
    return hashlib.sha1(msg).hexdigest()

def shortSHA(msg):
    return longSHA(msg)[:8]

