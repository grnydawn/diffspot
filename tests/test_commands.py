# -*- coding: utf-8 -*-

from .context import diffspot
import os
import shutil
import pytest

proj = os.path.join(os.path.dirname(__file__), 'myproj')
prog = os.path.join(os.path.dirname(__file__), 'prog/fort/app1')

def test_clear():
    shutil.rmtree(proj, ignore_errors=True)

def test_init():
    test_clear()
    diffspot.main(['init', proj])

def test_register():
    test_init()
    os.chdir(proj)
    diffspot.main(['register', prog])

def test_record():
    test_register()
    diffspot.main(['record'])

def test_execute():
    test_register()
    diffspot.main(['execute', 'make run',
        '--prerun', 'make clean; make build',
        '--postrun', 'make clean', '--cwd', prog])
