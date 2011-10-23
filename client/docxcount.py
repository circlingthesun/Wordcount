#! /usr/bin/python

import sys, shutil, os
import zipfile
from xml.sax.handler import ContentHandler
from xml import sax

def getXml(filename):
    with zipfile.ZipFile(filename) as myzip:
        fname = myzip.extract('word/document.xml', '.')
        val =  open(fname).read()
        shutil.rmtree(os.path.dirname(fname))
        return val

class textHandler(ContentHandler):
    text = []
    def characters(self, ch):
        self.text.append(ch.encode("utf-8"))

def gettext(xmldata):
    handler = textHandler()
    sax.parseString(xmldata, handler)
    return " ".join(handler.text)
        
def wordcount(text):
    # assumes words are separated by whitespace
    print text.split(None)
    return len(text.split(None))

def countdocx(filename):
    xml = getXml(filename)
    text = gettext(xml)
    return wordcount(text)

if __name__ == '__main__':        
    try:
        print countdocx(sys.argv[1])  
    except:    
        exit()   
