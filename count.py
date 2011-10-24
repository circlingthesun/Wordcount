#!/usr/bin/python
import os, json, dateutil.parser
from datetime import datetime, timedelta
from flask import Flask
from flask import request
import sqlite3

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
                Date.prototype.addHours= function(h){
                    this.setHours(this.getHours()+h);
                    return this;
                }

                $.getJSON("/json", function(datas) {
                    //console.log(datas);

                    for (series in datas) {
                        //console.log(datas[series]);
                        for (d in datas[series]["data"]) {
                            //console.log(datas[series]["data"][d]);
                            
                            datas[series]["data"][d][0] = Date.parse(datas[series]["data"][d][0]) + 2 * 60 * 60 * 1000;
                        }

                    }

                    chart = new Highcharts.Chart({
                        chart: {
                            renderTo: 'container',
                            zoomType: 'x',
                            type: 'spline'
                        },
                        title: {
                            text: 'The number of words written by great hackers'
                        },
                        xAxis: {
                            type: 'datetime',
                            maxzoom: 3600000,
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

                    function getMoar () {
                        $.getJSON("/json?min=5", function(dat) {
                            console.log("GOT MOAR");
                            for (series in dat) {

                                for (d in dat[series]["data"]) {
                                    dat[series]["data"][d][0] = Date.parse(datas[series]["data"][d][0]) + 2 * 60 * 60 * 1000;
                                    console.log(dat[series]["data"][d]);
                                }

                                var found = false;
                                for (serie in chart.series) {
                                    if (dat[series]["name"] == chart.series[serie]["name"]) {
                                        console.log("hurray");
                                        chart.series[serie].addPoint(dat[series]["data"][0]);
                                    }
                                    console.log(chart.series[serie]["name"]);
                                }
                            }
                        });
                    };

                    setInterval(getMoar(), 5);
                });
                
            });
                
        </script>
        
    </head>
    <body>
        
        <!-- 3. Add the container -->
        <div id="container" style="width: 800px; height: 400px; margin: 0 auto"></div>
        
        <a href="/static/client.zip">Download</a> the app to add your name.
                
    </body>
</html>"""
    return re

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
            final.append({ "name": name, "data": result[name]})

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
