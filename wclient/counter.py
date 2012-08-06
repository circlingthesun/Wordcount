#!/usr/bin/python
import sys, subprocess, os, time
import urllib
import ConfigParser
from docxcount import countdocx

config = ConfigParser.ConfigParser()
sfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.ini")
config.read(sfile)

# for non docx
interpreter = config.get('client', 'script_interpreter')
count_script = config.get('client', 'count_script')
count_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), count_script)

# for docx
docx_file = None

try:
    docx_file = config.get('client', 'docx_file')
    docx_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), docx_file)
except:
    pass

# settings
name = config.get('client', 'name')
url = config.get('client', 'update_url')
interval = int(config.get('client', 'update_interval'))

def run():
    while True:
    
        count = 0
        
        if docx_file :
            count = countdocx(docx_file)
        else:
            args = [interpreter, count_script]
            count,error = subprocess.Popen(args,stdout = subprocess.PIPE,
                    stderr= subprocess.PIPE).communicate()
            if error:
                print "Error %s" % error
        
        params = urllib.urlencode({'c': str(count), 'name': name})
        
        try:
            f = urllib.urlopen(url, params)
            print f.read()
        except:
            print "Cannot comunicate with server"
            
        time.sleep(interval)
    
if __name__ == "__main__":
    run()
