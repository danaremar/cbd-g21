import requests
import json
import datetime
import csv
from calendar import monthrange
import pymongo

START_YEAR = 2019
END_YEAR = 2020

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["ree-rest"]
my_col = my_db["demand"]

# DEMAND BY MONTH
def demand_by_month(year,month):
    days_of_month = monthrange(year, month)[1]
    month_f = str(month).zfill(2)
    url = 'https://apidatos.ree.es/es/datos/demanda/demanda-tiempo-real?start_date='+str(year)+'-'+month_f+'-01T00:00&end_date='+str(year)+'-'+month_f+'-'+str(days_of_month)+'T23:00&time_trunc=hour'
    return requests.get(url).json()["included"][0]["attributes"]["values"]


# DEMAND BY YEARS
def demand_by_years(start_year, end_year):
    years = range(start_year, end_year + 1)
    for y in years:
        for m in range(1,13):
            demand_by_month(y,m)

# INSERT INTO DB
def insert_into_db():
    #demand_list = demand_by_years(START_YEAR, END_YEAR)
    demand_list = demand_by_month(2020,2)
    print(demand_list[0:2])
    for i in demand_list:
        date_transformed = i["datetime"][0:19]
        my_dict = { "type": "demand", "value": i["value"], "datetime": datetime.datetime.strptime( date_transformed , "%Y-%m-%dT%H:%M:%S") }
        my_col.insert_one(my_dict)

# SCRIPT
insert_into_db()