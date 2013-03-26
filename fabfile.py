import os
from fabric.api import local, task

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
