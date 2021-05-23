import requests
import json
import datetime 
from calendar import monthrange
import pymongo
import matplotlib.pyplot as plt
import numpy
import arrow
from conf import DB_URL, DB_NAME, TYPE_BALANCE, TYPE_DEMAND, TYPE_CO2_NO_RENEWABLE, TYPE_PRICE_MARKET

my_client = pymongo.MongoClient(DB_URL)
my_db = my_client[DB_NAME]
my_col = my_db[TYPE_BALANCE]
my_col2 = my_db[TYPE_CO2_NO_RENEWABLE]
my_col3 = my_db[TYPE_DEMAND]
my_col4 = my_db[TYPE_PRICE_MARKET]



def by_principal_type(year, inicio, fin):

    renewable =  value_per_month("balance","Renovable",year, inicio, fin)
    no_renewable = value_per_month("balance","No-Renovable",year, inicio, fin)

    data = [renewable[0], no_renewable[0]]
    names = ["Renovable","No Renovable"]
    colors = ["#F34213","#2E2E3A"]
    
    #SEPARATED PIECE
    offset = (0, 0.1)

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors, explode=offset)
    plt.axis("equal")
    plt.show()

    return data


def by_child_type_no_renovable(year, inicio, fin):

    congeneracion = value_per_month("No-Renovable", "Turbina de vapor",year, inicio, fin) 
    vapor = value_per_month("No-Renovable", "Turbina de vapor", year, inicio, fin)
    bombeo = value_per_month("No-Renovable", "Turbinación bombeo", year, inicio, fin)
    nuclear = value_per_month("No-Renovable", "Nuclear", year, inicio, fin)
    ciclo = value_per_month("No-Renovable", "Ciclo combinado", year, inicio, fin)
    carbon = value_per_month("No-Renovable", "Carbón", year, inicio, fin)
    diesel = value_per_month("No-Renovable", "Motores diésel", year, inicio, fin)
    gas = value_per_month("No-Renovable", "Turbina de gas", year, inicio, fin)
    residuos = value_per_month("No-Renovable", "Residuos no renovables", year, inicio, fin)

    data = [congeneracion[0], vapor[0], bombeo[0], nuclear[0], diesel[0], ciclo[0], carbon[0], gas[0], residuos[0]]
    names = ["Cogeneración","Turbina de vapor","Turbinación bombeo","Nuclear","Motores diésel","Ciclo combinado","Carbón","Turbina de gas","Residuos no renovables"]
    colors = ["#F34213","#2E2E3A","#DE9151","#BC5D2E","#BBB8B2","#913827","#754634","#523A37","#995231"]
    offset = (0, 0.2, 0, 0, 0, 0, 0, 0.2, 0)

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors, explode=offset)
    plt.axis("equal")
    plt.show()

    return data



def by_child_type_renovable(year, inicio, fin):

    start = datetime.datetime(int(year), int(inicio), 1, 0, 0, 0)
    end = datetime.datetime(int(year), int(fin), 1, 0, 0, 0)

    hidraulica = value_per_month("Renovable","Hidráulica", year, inicio, fin)
    eolica = value_per_month("Renovable", "Eólica", year, inicio, fin)
    hidroeolica = value_per_month("Renovable", "Hidroeólica", year, inicio, fin)
    fotovoltaica = value_per_month("Renovable", "Solar fotovoltaica", year, inicio, fin)
    termica = value_per_month("Renovable", "Solar térmica", year, inicio, fin)
    otras = value_per_month("Renovable", "Otras renovables", year, inicio, fin)
    residuos = value_per_month("Renovable", "Residuos renovables", year, inicio, fin)

    data = [hidraulica[0], eolica[0], hidroeolica[0], fotovoltaica[0], termica[0], otras[0], residuos[0]]
    names = ["Hidráulica","Eólica","Hidroeólica","Solar fotovoltaica","Solar térmica","Otras renovables","Residuos renovables"]
    colors = ["#F34213","#2E2E3A","#DE9151","#BC5D2E","#BBB8B2","#913827","#754634"]

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors)
    plt.axis("equal")
    plt.show()

    return data



def co2_no_renewable(year, inicio, fin):

    carbon = value_per_month("co2_no_renewable","Carbón",year, inicio, fin)
    diesel = value_per_month("co2_no_renewable","Motores diésel",year, inicio, fin) 
    gas = value_per_month("co2_no_renewable","Turbina de gas",year, inicio, fin) 
    vapor = value_per_month("co2_no_renewable","Turbina de vapor",year, inicio, fin)
    ciclo = value_per_month("co2_no_renewable","Ciclo combinado",year, inicio, fin)
    congeneracion = value_per_month("co2_no_renewable","Cogeneración",year, inicio, fin)
    residuos = value_per_month("co2_no_renewable","Residuos no renovables",year, inicio, fin)

    data = [carbon[0], diesel[0], gas[0], vapor[0], ciclo[0], congeneracion[0], residuos[0]]
    names = ["Carbón","Motores diésel","Turbina de gas","Turbina de vapor","Ciclo combinado","Cogeneración","Residuos no renovables"]
    colors = ["#F34213","#2E2E3A","#DE9151","#BC5D2E","#BBB8B2","#913827","#754634"]
    offset = (0, 0.5, 0.2, 0, 0, 0, 0)

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors, explode=offset)
    plt.axis("equal")
    plt.show()

    return data



def demand_price_market(year):

    demand = value_per_month("demand","", year,0, 0)
    price = value_per_month("price_market","",year, 0, 0)

    fig = plt.figure() 
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    xx = range(len(demand))
    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

    ax1.bar(xx, demand, width=0.4, label="Demanda (KW/h)", color="#F34213", align='center')
    ax1.set_xticks(xx)
    ax1.set_xticklabels(meses)
    ax1.set_ylabel("Demanda")

    ax2.bar(xx, price, width=0.4, label="Precio de Mercado (€/KW/h)", color="#2E2E3A", align='center')
    ax2.set_xticks(xx)
    ax2.set_xticklabels(meses)
    ax2.set_ylabel("Precio de Mercado")

    plt.show()

    return [demand, price]


def value_per_month(aux,aux1,year,inicio, fin):
    average = []

    if str(aux)=="No-Renovable" or str(aux)=="Renovable":
        for month in range(inicio, fin+1):

            y = 0
            start = datetime.datetime(int(year), int(month), 1, 0, 0, 0)
            end = datetime.datetime(int(year), int(month), int(monthrange(year, month)[1]), 0, 00, 0) 

            data = my_col.find({ "principal_type":str(aux), "child_type":str(aux1), "datetime": {'$lt': end, '$gte': start}}).distinct("value")

            for x in data:

                    y = y+int(x)

        y=(y/int(monthrange(year, month)[1]))/(fin-inicio+1)
        average.append(y) 

    elif str(aux) == "demand" or str(aux) == "price_market":
        
            for month in range(1, 13):
                
                y = 0
                
                data = value_per_day(str(aux), int(year), int(month))

                for x in data:

                    y = y+int(x) 

                y=y/int(monthrange(year, month)[1])
                average.append(y)     

    elif str(aux)=="balance":

        for month in range(inicio, fin+1):

            y = 0

            start = datetime.datetime(int(year), int(month), 1, 0, 0, 0)
            end = datetime.datetime(int(year), int(month), int(monthrange(year, month)[1]), 0, 00, 0) 

            data = my_col.find({"principal_type":str(aux1), "datetime": {'$lt': end, '$gte': start}}).distinct("value")

            for x in data:

                    y = y+int(x)

        y=(y/int(monthrange(year, month)[1]))/(fin-inicio+1)
        average.append(y)

    elif str(aux)=="co2_no_renewable":

        for month in range(inicio, fin+1):

            y = 0

            start = datetime.datetime(int(year), int(month), 1, 0, 0, 0)
            end = datetime.datetime(int(year), int(month), int(monthrange(year, month)[1]), 0, 00, 0) 

            data = my_col2.find({"resource_type":str(aux1), "datetime": {'$lt': end, '$gte': start}}).distinct("value")

            for x in data:

                    y = y+int(x)

        y=(y/int(monthrange(year, month)[1]))/(fin-inicio+1)
        average.append(y)    

    return average


def value_per_day(aux,year,month):

    average = []
    days = int(monthrange(year, month)[1]) + 1

    for d in range(1, days):

        y = 0

        if str(aux) == "demand":
            start = datetime.datetime(int(year), int(month), d, 0, 0, 0)
            end = datetime.datetime(int(year), int(month), d, 23, 50, 0)

            for x in my_col3.find({"type":str(aux), "datetime": {'$lt': end, '$gte': start}}).distinct("value"):
                y = y + int(x)
            y = y/142

        
        elif str(aux) == "price_market":
            start = datetime.datetime(int(year), int(month), d, 0, 0, 0)
            end = datetime.datetime(int(year), int(month), d, 23, 0, 0)

            for x in my_col4.find({"type":str(aux), "datetime": {'$lt': end, '$gte': start}}).distinct("value"):
                y = y + int(x)
            y = y/24

        average.append(y)
    
    return average



# RETURN STRING MONTH IN SPANISH
def month(x, lang):
    return arrow.Arrow(2020,x,1).format('MMMM', locale=lang).capitalize()



# ASKS YEAR AND MONTHS
def query_time():
    
    this_year = datetime.datetime.today().year
    this_month = datetime.datetime.today().month
    
    print("Year:")
    year = int(input())
    print("\nStart month:")
    start_month = int(input())
    print("\nEnd month:")
    end_month = int(input())

    if start_month>=end_month or start_month>=12 or end_month>12 or start_month<0 or end_month<0 or year<0 or this_year<year or (this_year==year and (this_month<=start_month or this_month<=end_month)):
        print("\nNo valid data, please type correct times\n")
        [year, start_month, end_month] = query_time()
    
    return [year, start_month, end_month]



# STARTS
def main():
    [year, start_month, end_month] = query_time()

    i = month(start_month,'en')
    f = month(end_month,'en')

    print("\n############################################################")
    print("\nQuery from " + i + " to " + f + " of year " + str(year))
    print("\n############################################################\n\n")

    a = by_principal_type(year, start_month, end_month)
    b = by_child_type_renovable(year, start_month, end_month)
    c = by_child_type_no_renovable(year, start_month, end_month)
    d = co2_no_renewable(year, start_month, end_month)
    e = demand_price_market(year)

    print("Media de prodccuión Mw/h (Renovable): " + str(a[0]))
    print("\nMedia de prodccuión Mw/h (No Renovable): " + str(a[1]))

    print("\n\n############################################################")

    print("\nMedia de prodccuión Mw/h (Hidráulica): " + str(b[0]))
    print("\nMedia de prodccuión Mw/h (Eólica): " + str(b[1]))
    print("\nMedia de prodccuión Mw/h (Hidroeólica): " + str(b[2]))
    print("\nMedia de prodccuión Mw/h (Solar fotovoltaica): " + str(b[3]))
    print("\nMedia de prodccuión Mw/h (Solar térmica): " + str(b[4]))
    print("\nMedia de prodccuión Mw/h (Otras renovables): " + str(b[5]))
    print("\nMedia de prodccuión Mw/h (Residuos renovables): " + str(b[6]))

    print("\n\n############################################################")

    print("\nMedia de prodccuión Mw/h (Cogeneración): " + str(c[0]))
    print("\nMedia de prodccuión Mw/h (Turbina de vapor): " + str(c[1]))
    print("\nMedia de prodccuión Mw/h (Turbinación bombeo): " + str(c[2]))
    print("\nMedia de prodccuión Mw/h (Nuclear): " + str(c[3]))
    print("\nMedia de prodccuión Mw/h (Motores diésel): " + str(c[4]))
    print("\nMedia de prodccuión Mw/h (Ciclo combinado): " + str(c[5]))
    print("\nMedia de prodccuión Mw/h (Carbón): " + str(c[6]))
    print("\nMedia de prodccuión Mw/h (Turbina de gas): " + str(c[7]))
    print("\nMedia de prodccuión Mw/h (Residuos no renovables): " + str(c[8]))

    print("\n\n############################################################")

    print("\nMedia de prodccuión de toneladas de C02 (Carbón): " + str(d[0]))
    print("\nMedia de prodccuión de toneladas de C02 (Motores diésel): " + str(d[1]))
    print("\nMedia de prodccuión de toneladas de C02 (Turbina de gas): " + str(d[2]))
    print("\nMedia de prodccuión de toneladas de C02 (Turbina de vapor): " + str(d[3]))
    print("\nMedia de prodccuión de toneladas de C02 (Ciclo combinado): " + str(d[4]))
    print("\nMedia de prodccuión de toneladas de C02 (Cogeneración): " + str(d[5]))
    print("\nMedia de prodccuión de toneladas de C02 (Residuos no renovables): " + str(d[6]))

    print("\n\n############################################################")

    print("\nMedia por mes de prodccuión de Mw/h: " + str(e[0]))
    print("\nMedia por mes del precio del Mw/h: " + str(e[1]))

