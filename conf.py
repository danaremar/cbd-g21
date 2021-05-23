import os
import configparser

config = configparser.SafeConfigParser()

config.read("conf.cfg")

API_BASE_URL = config.get('rest','API_BASE_URL')

DB_URL = config.get('database','DB_URL')
DB_NAME = config.get('database','DB_NAME')

TYPE_BALANCE = config.get('data_types','TYPE_BALANCE')
TYPE_DEMAND = config.get('data_types','TYPE_DEMAND')
TYPE_CO2_NO_RENEWABLE = config.get('data_types','TYPE_CO2_NO_RENEWABLE')
TYPE_PRICE_MARKET = config.get('data_types','TYPE_PRICE_MARKET')