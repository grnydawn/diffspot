# -*- coding: utf-8 -*-

import os
import sh
import logging
import util
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
    """Create a project."""

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
    """Register objects into a project."""

    repo = util.cdrepo()

    index = os.path.join(repo, '.git', 'stateindex')
    config = configparser.ConfigParser()
    config.read(index)

    for idx, content in enumerate(contents):
        if os.path.exists(content):
            shaname = os.path.basename(content)+'_'+util.shortSHA(content)
            shapath = os.path.join(repo, STATES, shaname)
            sh.rm(shapath, '-rf')
            sh.cp(content, shapath, '-rpf')
            config.set('path', shaname, content)
        else:
            logging.error('{} is not found.'.format(content))

    sh.git.add('states')

    with open(index, 'w') as fh:
        config.write(fh)

def record(**kwargs):
    """Save states into a project"""

    if 'm' not in kwargs:
        kwargs['m'] ='None'

    repo = util.cdrepo()
    index = os.path.join(repo, '.git', 'stateindex')
    config = configparser.ConfigParser()
    config.read(index)

    for shaname, content in config.items('path'):
        shapath = os.path.join(repo, STATES, shaname)
        sh.rm(shapath, '-rf')
        sh.cp(content, shapath, '-rpf')

    timestamp = os.path.join(repo, 'states', 'timestamp')
    with open(timestamp, 'w') as fh:
        fh.write('{}\n'.format(util.datetimestr()))

    sh.git.add('states')
    sh.git.commit(**kwargs)


def execute(action, prerun, postrun, cwd):
    """Perform an action"""
    repo = util.cdrepo()

    if prerun is not None:
        retcode = subprocess.call(shlex.split(prerun), cwd=cwd, shell=True)
        if retcode != 0:
            import pdb; pdb.set_trace()

    record(m='before action')

    retcode = subprocess.call(shlex.split(action), cwd=cwd, shell=True)
    if retcode != 0:
        import pdb; pdb.set_trace()

    record(m='after action')

    if postrun is not None:
        retcode = subprocess.call(shlex.split(postrun), cwd=cwd, shell=True)
        if retcode != 0:
            import pdb; pdb.set_trace()
