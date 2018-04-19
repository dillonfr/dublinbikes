#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dublinbikes` package."""
import sys
sys.path.append('.')
import pytest
import unittest
import mysql.connector

from click.testing import CliRunner

from dublinbikes import dublinbikes
from dublinbikes import cli

class MyTest(unittest.TestCase):
    def test_query_API(self):
        result = dublinbikes.query_API("3")
        self.assertEqual(len(result), 12) #API gives back 12 pieces of info per station
        
    def test_station_list(self):
        result = dublinbikes.stations_list('Dublin.json')
        self.assertEqual(len(result), 100) #100 stations in the json file
    
    def test_single_station(self):
        result = dublinbikes.single_station_info("5")
        self.assertEqual(len(result), 8) #should return 8 pieces of info we want
        self.assertEqual(type(result['number']), int)
        self.assertEqual(result['number'], 5)
        self.assertLessEqual(result['bikes'], 50)
        
    def test_print_station_info(self):
        dhost="dublinbikes.cww5dmspazsv.eu-west-1.rds.amazonaws.com"
        dport=3306
        dbname="dublinbikes"
        duser="dbuser"
        dpassword="dbpassword1"
        cnx = mysql.connector.connect(user = duser, password = dpassword, 
                                      host = dhost, database=dbname)
            
            
        self.connection = cnx
        self.cur = cnx.cursor()
        self.cur.execute("SELECT latitude, longitude, bikes_available, stands_available FROM realtime WHERE number=\"1\"")
        print(self.cur.fetchall())
