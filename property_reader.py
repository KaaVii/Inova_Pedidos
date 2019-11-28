#!/usr/bin/python
import configparser

config = configparser.RawConfigParser()
config.read('config.properties')

#print(config.get('DatabaseSe ction', 'database.dbname'))

def getConfig(section, option):
    result = config.get(section,option)
    return result
