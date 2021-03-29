# encoding=utf8

import time
from datetime import datetime
import json

import flask
from flask import Flask, render_template
from markupsafe import escape

import weather_stealer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/date")
def date():
    now =  datetime.utcnow()
    date = {"day": now.day, "month": now.month , "year": now.year, "weekday": now.weekday() }
    date = json.dumps(date)
    resp = flask.Response(str(date))
    resp.headers["Content-Type"] = "application/json"
    return resp

## TODO: select unix or utc 
@app.route("/time")
def times():
    unix_time = time.time()
    now = datetime.utcnow()
    hour, minute, second = now.hour, now.minute, now.second
    times = {"unix": unix_time, "hour": hour, "minute": minute, "second": second}
    times = json.dumps(times)
    resp = flask.Response(str(times))
    resp.headers["Content-Type"] = "application/json"
    return resp



@app.route("/weather/<location>")
def weather(location):
    return location




