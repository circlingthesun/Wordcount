#!/usr/bin/python
import os
from datetime import datetime
from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('counts.db', detect_types=sqlite3.PARSE_DECLTYPES)
c = conn.cursor()
sql = 'create table if not exists count (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME, name TEXT, count INTEGER)'
c.execute(sql)

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "count.txt")

@app.route("/")
def hello():
    conn = sqlite3.connect('counts.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute("SELECT max(id), date, name, count FROM count GROUP BY name")
    data = c.fetchall()

    re = ""
    re = re + """<html><head><style type="text/css">
                td, th {padding:0 30 0 0;}
                </style></head><body>
                <table border="1"><tr><th>Name</th><th>Words</th><th>Time</th></tr>"""
    re = re + "".join(["<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (n,c,d) for _id, d,n,c in data])
    re = re + """</table>
                <a href="/static/wordcount.tar.gz">Download word counter </a>
                </body></html>"""
    return re

@app.route("/update", methods=['POST', 'GET'])
def update():
    conn = sqlite3.connect('counts.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    
    count = int(request.form['c'])
    name = request.form['name']
    
    sql = 'insert into count (date, name, count) values ("%s", "%s", %d)' % (datetime.now(), name, count)
    c.execute(sql)
    conn.commit()
    
    return "updated"

@app.route("/test")
def test():
    return "works"

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=6543)
