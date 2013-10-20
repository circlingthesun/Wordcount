#!/usr/bin/python
import os, json, dateutil.parser
from datetime import datetime, timedelta
from flask import Flask
from flask import request
import sqlite3
from flask import render_template

app = Flask(__name__)

db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "counts.db")
conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
c = conn.cursor()
sql = 'create table if not exists count (id INTEGER PRIMARY KEY AUTOINCREMENT, d timestamp, name TEXT, count INTEGER)'
c.execute(sql)

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "count.txt")

@app.route("/")
def hello():

    #conn = sqlite3.connect('counts.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    #c = conn.cursor()
    #c.execute("SELECT max(id), d, name, count FROM count GROUP BY name")
    #data = c.fetchall()

    return render_template('index.html')

@app.route("/json", methods=['GET'])
def timedatas():
    try:
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        c = conn.cursor()
        minute = request.args.get('min', 10 * 24 * 60 * 60, type=int)

        c.execute('SELECT id, d as "[timestamp]", name, count FROM count WHERE d > ?', (datetime.now() - timedelta(minutes=minute),))

        data = c.fetchall()
        result = {}

        for (id, date, name, count) in data:
            if not name in result:
                result[name] = []
                result[name].append([date.isoformat(), count])
            elif date - dateutil.parser.parse(result[name][-1][0]) > timedelta(minutes=5):
                result[name].append([date.isoformat(), count])
            else: 
                c.execute('DELETE FROM count where id = ?', (id,))
                conn.commit()
        
        final = []
        for name in result:
            final.append({ "name": name, "id": name, "data": result[name]})

        return json.dumps(final)
    except Exception as e:
        return str(e)

@app.route("/update", methods=['POST', 'GET'])
def update():
    conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    
    try:
        count = int(request.form['c'])
        name = request.form['name']

        if name == "Nobody":
            return "Please set your username."
        
        sql = 'insert into count(d, name, count) values (?, ?, ?)'
        c.execute(sql, (datetime.now(), name, count))
        conn.commit()
    except:
        conn.rollback();
    
    return "updated"

@app.route("/test")
def test():
    return "works"

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=7001)
