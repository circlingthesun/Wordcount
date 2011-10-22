#!/usr/bin/python
import sys, subprocess, os, time
import urllib
import ConfigParser

config = ConfigParser.ConfigParser()
sfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.ini")
config.read(sfile)

count_script = config.get('client', 'count_script')
count_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), count_script)

name = config.get('client', 'name')
url = config.get('client', 'update_url')
interval = int(config.get('client', 'update_interval'))

def run():
    while True:
        args = ["bash", count_script]
        count,error = subprocess.Popen(args,stdout = subprocess.PIPE,
                stderr= subprocess.PIPE).communicate()
        if error:
            print "Error %s" % error
        params = urllib.urlencode({'c': count, 'name': name})
        f = urllib.urlopen(url, params)
        print f.read()
        time.sleep(interval)
    

if __name__ == "__main__":
    run()
