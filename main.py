import requests
import json
from datetime import datetime
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


# INSERT BY MONTH INTO DB
def insert_into_db_by_month(year, month):
    demand_list = demand_by_month(year,month)

    for i in demand_list:
        date_string = i["datetime"][0:19]
        date = datetime.strptime( date_string , "%Y-%m-%dT%H:%M:%S")
        _id = datetime.timestamp(date)
        my_dict = { "_id": _id, "type": "demand", "value": i["value"], "datetime": date }
        my_col.insert_one(my_dict)

    print( "insert_into_db_by_month() - Inserted for " + str(month) + "/" + str(year) )



# INSERT INTO DB BY YEARS
def insert_into_db_by_years(start_year, end_year):
    years = range(start_year, end_year + 1)
    for y in years:
        for m in range(1,13):
            this_year = datetime.today().year
            this_month = datetime.today().month
            if this_year<=y and this_month<=m:
                # not allowes calls to future, stop and don't continue
                print("insert_into_db_by_years() - Future date")
                return
            insert_into_db_by_month(y, m)


# DROP COLLECTION
def drop():
    my_col.drop()


def run():
    drop()
    insert_into_db_by_years(START_YEAR, END_YEAR)

run()
