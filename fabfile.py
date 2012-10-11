from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['rickert.co.za']
env.user = 'rickert'
#env.password = ''
env.remote_dev = "rickert.co.za"
env.remote_dir = "/home/rickert/webapps/Wordcount.git"

code_dir = '/home/rickert/webapps/Wordcount'

def zipclient():
    local('zip -r wserver/static/client.zip wclient -x \*.pyc \*~ \*.ui')

def commit():
    zipclient()
    local("git add -p && git commit")

def push_to_remote():
    local("git push ssh://%(user)s@%(remote_dev)s/%(remote_dir)s master" % env)

def pull_remote():
    with cd(code_dir):
        #run("git reset --hard HEAD")
        run("git checkout master")
        run("git pull")
        #run("git reset --hard HEAD")
        run("source env/bin/activate && python setup.py develop")
        run("touch formative.wsgi")

def deploy():
    commit()
    push_to_remote()
    pull_remote()
    
def update():
    local("git pull ssh://%(user)s@%(remote_dev)s/%(remote_dir)s" % env)
