# -*- coding: utf-8 -*-

import os
import sh
import logging
from .util import shortSHA
import subprocess
import shlex
try:
    import configparser
except:
    import ConfigParser as configparser

STATES = 'states'
TESTS = 'tests'
MONITORS = 'monitors'

# create an empty project 
def init(repo):
    """Create directory for repo and initialize .git directory."""

    sh.git.init(repo)

    with open(os.path.join(repo, '.gitignore'), 'w') as fh:
        fh.write('*\n')
        fh.write('!{}\n'.format(STATES))
        fh.write('!{}/**\n'.format(STATES))

    os.mkdir(os.path.join(repo, STATES))
    os.mkdir(os.path.join(repo, TESTS))
    os.mkdir(os.path.join(repo, MONITORS))

    with open(os.path.join(repo, '.git', 'stateindex'), 'w') as fh:
        fh.write('[path]\n\n')
        fh.write('[script]\n\n')

# add file content to project
def register(contents):
    """Add file contents."""

    index = os.path.join(os.getcwd(), '.git', 'stateindex')
    config = configparser.ConfigParser()
    config.read(index)

    for idx, content in enumerate(contents):
        if os.path.exists(content):
            shaname = os.path.basename(content)+'_'+shortSHA(content)
            sh.cp(content, os.path.join(os.getcwd(), STATES, shaname), '-rpf')
            sh.git.add('states')
            config.set('path', shaname, content)
        else:
            logging.error('{} is not found.'.format(content))

    with open(index, 'w') as fh:
        config.write(fh)

def record():

    # copy all contents into states

    sh.git.commit(m='test')


def execute(action, prerun, postrun, cwd):
    """Perform an action"""

    import pdb; pdb.set_trace()
    if prerun is not None:
        subprocess.call(shlex.split(prerun), cwd=cwd, shell=True)

    # copy all contents into states

    sh.git.commit(m='before action')

    subprocess.call(shlex.split(action), cwd=cwd, shell=True)

    # copy all contents into states

    sh.git.commit(m='after action')

    if postrun is not None:
        subprocess.call(shlex.split(postrun), cwd=cwd, shell=True)
