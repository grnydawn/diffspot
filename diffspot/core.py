# -*- coding: utf-8 -*-
from . import helpers

import logging

logging.debug('in core')

def get_hmm():
    """Get a thought."""
    return 'hmmm...'


def hmm():
    """Contemplation..."""
    if helpers.get_answer():
        print(get_hmm())
