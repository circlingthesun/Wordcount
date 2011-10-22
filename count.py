#!/usr/bin/python
import os, json
from datetime import datetime
from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('counts.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
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

    re = """<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Many words have been written</title>
        
        
        <!-- 1. Add these JavaScript inclusions in the head of your page -->
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
        <script type="text/javascript" src="static/js/highcharts.js"></script>
        
        <!-- 1a) Optional: add a theme file -->
        <!--
            <script type="text/javascript" src="static/js/themes/gray.js"></script>
        -->
        
        <!-- 1b) Optional: the exporting module -->
        <script type="text/javascript" src="static/js/modules/exporting.js"></script>
        
        
        <!-- 2. Add the JavaScript to initialize the chart on document ready -->
        <script type="text/javascript">
        
            var chart;
            $(document).ready(function() {
                $.getJSON("/json", function(datas) {
                    console.log(datas);
                    chart = new Highcharts.Chart({
                        chart: {
                            renderTo: 'container',
                            type: 'spline'
                        },
                        title: {
                            text: 'The number of words written by great hackers'
                        },
                        xAxis: {
                            type: 'datetime',
                            dateTimeLabelFormats: { // don't display the dummy year
                                month: '%e. %b',
                                year: '%b'
                            }
                        },
                        yAxis: {
                            title: {
                                text: 'Words'
                            },
                            min: 0
                        },
                        tooltip: {
                            formatter: function() {
                                    return '<b>'+ this.series.name +'</b><br/>'+
                                    Highcharts.dateFormat('%e. %b', this.x) +': '+ this.y +' m';
                            }
                        },
                        series: datas
                    });
                });
                
            });
                
        </script>
        
    </head>
    <body>
        
        <!-- 3. Add the container -->
        <div id="container" style="width: 800px; height: 400px; margin: 0 auto"></div>
        
                
    </body>
</html>"""
    return re

@app.route("/json")
def timedatas():
    conn = sqlite3.connect('counts.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute('SELECT id, d as "d [timestamp]", name, count FROM count')
    data = c.fetchall()
    print data
    result = {}

    for (id, date, name, count) in data:
        if not name in result:
            result[name] = []
        result[name].append([date.isoformat(), count])
    
    final = []
    for name in result:
        final.append({ "name": name, "data": result[name]})

    return json.dumps(final)

@app.route("/update", methods=['POST', 'GET'])
def update():
    conn = sqlite3.connect('counts.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    
    try:
        count = int(request.form['c'])
        name = request.form['name']
        
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
    app.run(host="0.0.0.0", port=6543)
