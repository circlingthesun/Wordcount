from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['words.jacklab.co.za']
env.user = 'rickert'
#env.password = ''
env.remote_dev = "rickert.co.za"
env.remote_dir = "/home/rickert/Wordcount.git"
code_dir = '/home/rickert/Wordcount'
repo = "ssh://git@github.com:circlingthesun/Wordcount.git"

def zipclient():
    local('zip -r wserver/static/client.zip wclient -x \*.pyc \*~ \*.ui')

def commit():
    zipclient()
    with settings(warn_only=True):
        local("git add -p && git commit")

def push_to_remote():
    local("git push origin master")
    #local("git push ssh://%(user)s@%(remote_dev)s/%(remote_dir)s master" % env)

def pull_remote():
    with cd(code_dir):
        #run("git reset --hard HEAD")
        #run("git checkout master")
        run("git pull")
        #run("git reset --hard HEAD")
        run("source env/bin/activate && python setup.py develop")

def deploy():
    commit()
    push_to_remote()
    pull_remote()
    
def update():
    local("git pull %s" % repo)
