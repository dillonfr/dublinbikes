# -*- coding: utf-8 -*-

"""Main module."""
import requests
import json
import csv
import pandas
import mysql.connector
from pprint import pprint
from datetime import datetime
from _datetime import date




staticData = json.load(open('Dublin.json'))

dubUrl = "https://api.jcdecaux.com/vls/v1/stations/30?contract=Dublin&apiKey=066552409dad0809af4e338d67817a8d931d697d"
apiKey = "066552409dad0809af4e338d67817a8d931d697d"
        
def query_API(stationNumber):
    r = requests.get('https://api.jcdecaux.com/vls/v1/stations/' + str(stationNumber) + '?contract=Dublin&apiKey=' + apiKey)
    r = r.json() 
    return r

def stations_list(fileName):
    data = json.load(open(fileName))
    stations = []
    for i in data:
        stations.append(i["number"])
        stations.sort()
    return stations
    
def single_station_info(stationNumber):
    g = query_API(stationNumber) 
    d = datetime.now().date()
    t = datetime.now().time()
    station_info = {'number': g["number"], 
                    'name': g["name"], 
                    'latitude': g["position"]["lat"], 
                    'longitude': g["position"]["lng"], 
                    'bikes': g["available_bikes"], 
                    'stands': g["available_bike_stands"],
                    'time': t,
                    'date': d}
    
    
    return station_info
        
    
class Database:
    def __init__(self):
        
        from mysql.connector import errorcode
        try:
            dhost="dublinbikes.cww5dmspazsv.eu-west-1.rds.amazonaws.com"
            dport=3306
            dbname="dublinbikes"
            duser="dbuser"
            dpassword="dbpassword1"
            cnx = mysql.connector.connect(user = duser, password = dpassword, 
                                      host = dhost, database=dbname)
            
            
            self.connection = cnx
            self.cur = cnx.cursor()
            print("connected")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
         
        
    def add_station_info(self, statInfo):
        query = "INSERT INTO stations (number, name, latitude, longitude, bikes_available, stands_available, time, date) " \
                    "VALUES (%(number)s, %(name)s, %(latitude)s, %(longitude)s, %(bikes)s, %(stands)s, %(time)s, %(date)s) "
        
        self.cur.execute(query, statInfo)
        self.connection.commit()
        print("info added")
        
    def update_realtime_info(self, statInfo):
        query = """ UPDATE realtime 
                    SET bikes_available = %(bikes)s,
                    stands_available = %(stands)s,
                    time = %(time)s,
                    date = %(date)s
                    WHERE number = %(number)s"""
        self.cur.execute(query, statInfo)
        self.connection.commit()
        print("updated")
        
    
        
    def close_db(self):
        self.cur.close()
        self.connection.close()
      