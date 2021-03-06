import requests
import json
from datetime import datetime
from calendar import monthrange
import pymongo
from conf import API_BASE_URL, DB_URL, DB_NAME, TYPE_BALANCE, TYPE_DEMAND, TYPE_CO2_NO_RENEWABLE, TYPE_PRICE_MARKET

my_client = pymongo.MongoClient(DB_URL)
my_db = my_client[DB_NAME]

TIME_EXP = "%Y-%m-%dT%H:%M:%S"


# STRING TO PRINT
def inserted_info(year, month, data_type):
    return str(month) + "/" + str(year) + " - Inserted for " + data_type



# BALANCE BY MONTH
def rest_anided_by_month(year,month,data_type):
    days_of_month = monthrange(year, month)[1]
    month_f = str(month).zfill(2)
    
    if data_type==TYPE_BALANCE:
        category = '/balance/balance-electrico'
    elif data_type==TYPE_CO2_NO_RENEWABLE:
        category = '/generacion/no-renovables-detalle-emisiones-CO2'
    else:
        return

    time_trunc = 'day'

    url = API_BASE_URL + category + '?start_date=' + str(year) + '-' + month_f + '-01T00:00&end_date=' + str(year) + '-' + month_f + '-' + str(days_of_month) + 'T23:00&time_trunc=' + time_trunc
    res = requests.get(url).json()
    return res["included"]



# INSERT BALANCE BY MONTH INTO DB
def insert_balance_by_month(year, month):
    data_type = TYPE_BALANCE
    balance_list = rest_anided_by_month(year, month, data_type)
    my_col = my_db[data_type]

    for i in balance_list:
        
        data_energy_type = i["attributes"]
        principal_type = data_energy_type["title"]

        for j in data_energy_type["content"]:
            child_type = j["type"]

            for k in j["attributes"]["values"]:
                date_string = k["datetime"][0:19]
                date = datetime.strptime( date_string , TIME_EXP)
                my_dict = {"type": data_type, "percentage": k["percentage"], "value": k["value"], "datetime": date,
                    "principal_type": principal_type, "child_type": child_type }
                my_col.insert_one(my_dict)

    print(inserted_info(year, month, data_type))



# INSERT CO2 BY MONTH INTO DB
def insert_co2_by_month(year, month):
    data_type = TYPE_CO2_NO_RENEWABLE
    balance_list = rest_anided_by_month(year, month, data_type)
    my_col = my_db[data_type]

    for i in balance_list:
        
        data_energy_type = i["attributes"]
        resource_type = data_energy_type["title"]

        for j in data_energy_type["values"]:
            
            date_string = j["datetime"][0:19]
            date = datetime.strptime( date_string , TIME_EXP)
            my_dict = { "type": data_type, "percentage": j["percentage"], "value": j["value"], "datetime": date,
                "resource_type": resource_type, "magnitude": "tCO2 eq." }
            my_col.insert_one(my_dict)

    print(inserted_info(year, month, data_type))



# QUERY BY MONTH
def rest_query_by_month(year,month,data_type):
    days_of_month = monthrange(year, month)[1]
    month_f = str(month).zfill(2)
    
    if data_type==TYPE_PRICE_MARKET:
        category = '/mercados/precios-mercados-tiempo-real'
    elif data_type==TYPE_DEMAND:
        category = '/demanda/demanda-tiempo-real'
    else:
        return

    time_trunc = 'hour'

    url = API_BASE_URL + category + '?start_date=' + str(year) + '-' + month_f + '-01T00:00&end_date=' + str(year) + '-' + month_f + '-' + str(days_of_month) + 'T23:00&time_trunc=' + time_trunc
    res = requests.get(url).json()
    return res["included"][0]["attributes"]["values"]



# INSERT BY MONTH INTO DB
def insert_into_db_by_month(year, month, data_type):
    demand_list = rest_query_by_month(year, month, data_type)
    my_col = my_db[data_type]

    for i in demand_list:
        date_string = i["datetime"][0:19]
        date = datetime.strptime( date_string , TIME_EXP)
        my_dict = { "type": data_type, "percentage": i["percentage"], "value": i["value"], "datetime": date }
        my_col.insert_one(my_dict)

    print(inserted_info(year, month, data_type))



# INSERT INTO DB BY YEARS
def insert_into_db_by_years(start_year, end_year):
    years = range(start_year, end_year + 1)
    for y in years:
        for m in range(1,13):
            this_year = datetime.today().year
            this_month = datetime.today().month
            if this_year<=y and this_month<=m:
                # not allowes calls to future, stop and don't continue
                print("FUTURE - Skipping process")
                return

            insert_balance_by_month(y, m)
            insert_into_db_by_month(y, m, TYPE_DEMAND)
            insert_co2_by_month(y, m)
            insert_into_db_by_month(y, m, TYPE_PRICE_MARKET)



# DROP COLLECTION
def drop_db():
    my_client.drop_database(DB_NAME)



# DROP DATABASE AND INSERT ALL DATA
def load_data(start_year, end_year):
    drop_db()
    print("\n\n##############################")
    print("LOADING DATA")
    print("##############################\n\n")
    print("MONTH/YEAR - INFO\n")
    insert_into_db_by_years(start_year, end_year)



# ASKS DATES TO USER
def request_dates():
    this_year = datetime.today().year

    print('Start year:')
    start_year = int(input())

    print('End year:')
    end_year = int(input())

    if this_year<end_year or end_year<0 or this_year<start_year or start_year<0:
        print('\nPlease insert correct years:')
        [start_year, end_year] = request_dates()

    return [start_year, end_year]



# CONFIRM & LOAD DATA
def load_data_selected():
    [start_year, end_year] = request_dates()

    print('\nDo you want to delete DB and load new data?')
    second_option = str(input())

    if ['Y', 'YES', 'S', 'SI'].__contains__(second_option.capitalize()):
        load_data(start_year, end_year)