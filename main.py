import requests
import json
import datetime
import csv
from calendar import monthrange

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

# SCRIPT
r = demand_by_month(2020,2)
print(r[0])