from flask import render_template, jsonify, json
from app import app
import os
import json
import sys
import re




        
    
        
     #first is integer second is dict
    # if all else fails use re
    
@app.route('/', methods=['GET'])
def index():
    with app.open_resource('Dublin.json', 'r') as f:
        mydata = json.load(f)
        location = []
        name = []
        number = []
        address = []
        lat = []
        long = []
        j=0
        for i in mydata:
            number.append(mydata[j]['number'])
            name.append(mydata[j]['name'])
            address.append(mydata[j]['address'])
            lat.append(mydata[j]['latitude'])
            long.append(mydata[j]['longitude'])

            j+=1
        address = json.dumps(address).replace("\'", "\\'")
        name = json.dumps(name).replace("\'", "\\'")   
        number = json.dumps(number)
        lat = json.dumps(lat)
        long = json.dumps(long)    
    returnDict = {}
    returnDict['user'] = 'User123'
    returnDict['title'] = 'Dublin Bikes'
    return render_template("index.html", **returnDict, number=number, address=address, lat=lat, long=long)

