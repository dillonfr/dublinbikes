# -*- coding: utf-8 -*-

"""Console script for dublinbikes."""
import sys
sys.path.append('.')
import click
import dublinbikes
import mysql.connector
import datetime
import time
from mysql.connector import errorcode


@click.command()
def main(args=None):
    """Console script for dublinbikes."""
    stationList = dublinbikes.stations_list('Dublin.json')
    
    while True:   
        dubStationInfo = dublinbikes.Database()
        for i in stationList:
            k = dublinbikes.single_station_info(i)
            dubStationInfo.add_station_info(k)
        
        time.sleep(300)

    dubStationInfo.close_db()
    
def update(args=None):
    stationList = dublinbikes.stations_list('Dublin.json')
    
    while True:
        dubStationInfo = dublinbikes.Database()
        for i in stationList:
            k = dublinbikes.single_station_info(i)
            dubStationInfo.update_realtime_info(k)
        
        time.sleep(300)
    
    dubStationInfo.close_db()


#run main to insert into big table of all stations
#main()
#run update to update the realtime info
update()
