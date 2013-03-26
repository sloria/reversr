"""
Starter fabfile for deploying the PROJECTNAME project.

Change all the things marked CHANGEME. Other things can be left at their
defaults if you are happy with the default layout.
"""

import os
from fabric.api import run, local, env, cd, task
#from fabric.decorators import runs_once
#from fabric.context_managers import cd, lcd, settings, hide


# Python version
PYTHON_BIN = "python2.7"
PYTHON_PREFIX = ""  # e.g. /usr/local  Use "" for automatic
PYTHON_FULL_PATH = "%s/bin/%s" % (PYTHON_PREFIX, PYTHON_BIN) if PYTHON_PREFIX else PYTHON_BIN

# Javascript directory
JAVASCRIPT_DIR = os.path.join('static', 'js')
# Coffeescript directory
COFFEE_DIR = os.path.join('static', 'coffee')


@task
def clean(remote=False):
    '''Clears temporary directories in the media/audio directory.'''
    local('rm -rf media/audio/tmp*')
    if remote:
        local('heroku run "rm -rf /app/media/audio/tmp*"')
    print 'Cleaned up.'

@task
def coffee(watch=1):
    '''
    Compiles Coffeescript files.

    Enters watch mode by default when you run:
        >> fab coffee
    To do a one-time compile, run:
        >> fab coffee:watch=0
    '''

    base_command = 'coffee -o {} '.format(JAVASCRIPT_DIR)
    coffee_files = "{}/*.coffee".format(COFFEE_DIR)
    if watch == 1:
        print "Watching .coffee files in {} to {}".format(COFFEE_DIR, JAVASCRIPT_DIR)
        command = base_command + '-cw ' + coffee_files
    else:
        print "Compiling .coffee files in {} and compiling them to {}".format(COFFEE_DIR, JAVASCRIPT_DIR)
        command = base_command + '-c ' + coffee_files
    local(command)

@task
def watchmedo():
    """
    Watches the file system for changes of ``*.py`` files and executes the tests
    whenever you save a file.
    """ 
    cmd = 'watchmedo shell-command --recursive --ignore-directories --patterns="*.py" --wait --command="fab test:unit=1,webtest=1" .'
    local(cmd)

@task
def test(unit=1, webtest=1):
    """
    Runs the tests.
    """
    command = 'nosetests --verbosity=2'
    if all == 0:
        if int(unit) == 0:
            command += " --exclude='unit_tests' "
        if int(webtest) == 0:
            command += " --exclude='webtest_tests' "
    local(command)
