# -*- coding: utf-8 -*-

"""Main module."""
import requests
import json
import pandas
from pprint import pprint
from datetime import datetime


#Use json.load to read in the Dublin.json file
#Dublin.json contains static information about all the bike stations

staticData = json.load(open('Dublin.json'))




#pprint(staticData)
#print(staticData[0]["name"])
#print(staticData[57]["latitude"])

apiKey = "2603fd2d637c4e725086b2d6628df910fa9337fd"
base = 'https://api.jcdecaux.com/vls/v1/'

response = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&" + apiKey + "={api_key}")

print(response.status_code)

def query_API(url):
    # Send a query to the API and decode the bytes it returns
    query = urlopen(url).read().decode('utf-8')
    # Return the obtained string as a dictionary
    return json.loads(query)

def stations_list(city):
    url = base + 'stations/?contract={0}&apiKey={1}'.format(city, apiKey)
    data = query_API(url)
    return data

def timestamp_to_ISO(timestamp):
    moment = datetime.fromtimestamp(timestamp / 1000)
    return moment.time().isoformat()

def information(city):
    # Collect JSON data
    data = stations_list(city)
    # Convert it to a dataframe
    df = pd.io.json.DataFrame(data)
    # The positions are embedded so they have to be extracted
    positions = df.position.apply(pd.Series)
    df['latitude'] = positions['lat']
    df['longitude'] = positions['lng']
    # Make the timestamps human readable
    df['last_update'] = df['last_update'].apply(timestamp_to_ISO)
    return df[['available_bikes', 'last_update', 'name', 'latitude',
               'longitude', 'available_bike_stands', 'bike_stands',
               'status']]
    

information(dublin)
#print(df.dtypes)