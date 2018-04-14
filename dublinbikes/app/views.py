from flask import render_template, jsonify, json, g, Flask
from sqlalchemy import create_engine
from app import app
import os
import json
import sys
import re
import requests
import sqlite3
from _sqlite3 import Row
import pandas as pd


def connect_to_database():
    engine = create_engine("mysql+mysqldb://dbuser:dbpassword1@dublinbikes.cww5dmspazsv.eu-west-1.rds.amazonaws.com/dublinbikes", echo=True)
    return engine

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.route("/stations")
def get_all_stations():
    engine = get_db()
    sql = "SELECT number, name, latitude, longitude, bikes_available, stands_available from realtime;"
    rows = engine.execute(sql).fetchall()
    
    return jsonify(stations=[dict(row.items()) for row in rows])

@app.route("/weather")
def query_weather():
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dublin&APPID=094f61b4b2da3c4541e43364bab71b0b')
    r = r.json()
    weatherInfo= {'main': r['weather'][0]['main'], 
                     'detail': r['weather'][0]['description'], 
                     'temp': r['main']['temp'], 
                     'wind': r['wind']['speed'],
                     'icon': r['weather'][0]['icon']}
    print(weatherInfo)
    return jsonify(weatherInfo=weatherInfo)


@app.route("/available/<int:station_id>")
def get_stations(station_id):
    engine = get_db()
    data = []
    rows = engine.execute("SELECT bikes_available FROM realtime WHERE number = {};".format(station_id))
    for row in rows:
        data.append(dict(row))
        
    return jsonify(available=data)

@app.route("/dataframe/<int:station_id>")
def get_dataframe(station_id):
    engine = get_db()
    #params = {"number": station_id}
    sql = """select bikes_available, stands_available, time from stations where number= {} and date = '2018-04-09';""".format(station_id)
    #.format(**params)
    df = pd.read_sql_query(sql, engine)
    df = df.to_json(orient='index')
    df = json.loads(df)
    return jsonify(df=df)


@app.route('/', methods=['GET'])
def index():
    returnDict = {}
    returnDict['user'] = 'User123'
    returnDict['title'] = 'Dublin Bikes'
    return render_template("index1.html", **returnDict)
    


