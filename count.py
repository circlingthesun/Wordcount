#!/usr/bin/python
from flask import Flask
from flask import request
import os

app = Flask(__name__)

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "count.txt")

@app.route("/")
def hello():
    f = open(filename, 'r').read()    
    people = [i.split('~') for i in f.split('\n') if i]
    re = ""
    re = re + """<html><head><style type="text/css">
                td, th {padding:0 30 0 0;}
                </style></head><body>
                <table border="1"><tr><th>Name</th><th>Words</th></tr>"""
    re = re + "".join(["<tr><td>%s</td><td>%s</td></tr>" % (p,w) for p,w in people])
    re = re + """</table>
                <a href="/static/wordcount.tar.gz">Download word counter </a>
                </body></html>"""
    return re

@app.route("/update", methods=['POST', 'GET'])
def update():

    count = request.form['c']
    name = request.form['name']

    f = open(filename, 'r').read()
    people = [i.split('~') for i in f.split('\n') if i]
    
    f = open(filename, 'w')
        
    f.write("%s~%s\n" % (name, count))
    
    for p in people:
        if p[0] != name:
            f.write("%s~%s\n" % (p[0], p[1]))

    f.close()
    return "updated"

@app.route("/test")
def test():
    return "works"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6543)
