import requests
import json
import datetime 
from calendar import monthrange
import pymongo
import matplotlib.pyplot as plt
import numpy

# PERIOD LOAD
START_YEAR = 2020
END_YEAR = 2020

# DATABASE CONFIG
DB_URL = "mongodb://localhost:27017/"
DB_NAME = "ree-rest"

my_client = pymongo.MongoClient(DB_URL)
my_db = my_client[DB_NAME]
my_col = my_db["balance"]
my_col2 = my_db["co2_no_renewable"]
my_col3 = my_db["demand"]
my_col4 = my_db["price_market"]


def by_principal_type(inicio, fin):

    start = datetime.datetime(int(START_YEAR), int(inicio), 1, 0, 0, 0)
    end = datetime.datetime(int(END_YEAR), int(fin), 1, 0, 0, 0)
    
    renovable = my_col.find({"type":"balance", "principal_type":"Renovable", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    no_renovable = my_col.find({"type":"balance", "principal_type":"No-Renovable", "datetime": {'$lt':end, '$gte':start}}).distinct("value")

    p_renovable = value_balance(renovable)
    p_no_renovable = value_balance(no_renovable)

    data = [p_renovable, p_no_renovable]
    names = ["Renobable","No Renobable"]
    colors = ["#F34213","#2E2E3A"]
    #SEPARATED PIECE
    desfase = (0, 0.1)

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors, explode=desfase)
    plt.axis("equal")
    plt.show()






def value_balance(collection):

    y = 0 

    for x in collection:

        y = y + int(x)
    
    return y




def by_child_type_no_renovable(inicio, fin):

    start = datetime.datetime(int(START_YEAR), int(inicio), 1, 0, 0, 0)
    end = datetime.datetime(int(END_YEAR), int(fin), 1, 0, 0, 0)

    congeneracion = my_col.find({"type":"balance", "principal_type":"No-Renovable", "child_type":"Cogeneración", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    vapor = my_col.find({"type":"balance", "principal_type":"No-Renovable", "child_type":"Turbina de vapor", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    bombeo = my_col.find({"type":"balance", "principal_type":"No-Renovable", "child_type":"Turbinación bombeo", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    nuclear = my_col.find({"type":"balance", "principal_type":"No-Renovable", "child_type":"Nuclear", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    ciclo = my_col.find({"type":"balance", "principal_type":"No-Renovable", "child_type":"Ciclo combinado", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    carbon = my_col.find({"type":"balance", "principal_type":"No-Renovable", "child_type":"Carbón", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    diesel = my_col.find({"type":"balance", "principal_type":"No-Renovable", "child_type":"Motores diésel", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    gas = my_col.find({"type":"balance", "principal_type":"No-Renovable", "child_type":"Turbina de gas", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    residuos = my_col.find({"type":"balance", "principal_type":"No-Renovable", "child_type":"Residuos no renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")

    p_congeneracion = value_balance(congeneracion)
    p_vapor = value_balance(vapor)
    p_bombeo = value_balance(bombeo)
    p_nuclear = value_balance(nuclear)
    p_diesel = value_balance(diesel)
    p_ciclo = value_balance(ciclo)
    p_carbon = value_balance(carbon)
    p_gas = value_balance(gas)
    p_residuos = value_balance(residuos)

    data = [p_congeneracion, p_vapor, p_bombeo, p_nuclear, p_diesel, p_ciclo, p_carbon, p_gas, p_residuos]
    names = ["Cogeneración","Turbina de vapor","Turbinación bombeo","Nuclear","Motores diésel","Ciclo combinado","Carbón","Turbina de gas","Residuos no renovables"]
    colors = ["#F34213","#2E2E3A","#DE9151","#BC5D2E","#BBB8B2","#913827","#754634","#523A37","#995231"]
    desfase = (0, 0.2, 0, 0, 0, 0, 0, 0.2, 0)

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors, explode=desfase)
    plt.axis("equal")
    plt.show()






def by_child_type_renovable(inicio, fin):
    
    start = datetime.datetime(int(START_YEAR), int(inicio), 1, 0, 0, 0)
    end = datetime.datetime(int(END_YEAR), int(fin), 1, 0, 0, 0)

    hidraulica = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Hidráulica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    eolica = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Eólica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    hidroeolica = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Hidroeólica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    fotovoltaica = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Solar fotovoltaica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    termica = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Solar térmica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    otras = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Otras renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    residuos = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Residuos renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")

    p_hidraulica = value_balance(hidraulica)
    p_eolica = value_balance(eolica)
    p_hidroeolica = value_balance(hidroeolica)
    p_fotovoltaica = value_balance(fotovoltaica)
    p_termica = value_balance(termica)
    p_otras = value_balance(otras)
    p_residuos = value_balance(residuos)

    data = [p_hidraulica, p_eolica, p_hidroeolica, p_fotovoltaica, p_termica, p_otras, p_residuos]
    names = ["Hidráulica","Eólica","Hidroeólica","Solar fotovoltaica","Solar térmica","Otras renovables","Residuos renovables"]
    colors = ["#F34213","#2E2E3A","#DE9151","#BC5D2E","#BBB8B2","#913827","#754634"]


    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors)
    plt.axis("equal")
    plt.show()

def by_child_type_renovable(inicio, fin):
    
    start = datetime.datetime(int(START_YEAR), int(inicio), 1, 0, 0, 0)
    end = datetime.datetime(int(END_YEAR), int(fin), 1, 0, 0, 0)

    hidraulica = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Hidráulica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    eolica = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Eólica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    hidroeolica = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Hidroeólica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    fotovoltaica = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Solar fotovoltaica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    termica = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Solar térmica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    otras = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Otras renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    residuos = my_col.find({"type":"balance", "principal_type":"Renovable", "child_type":"Residuos renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")

    p_hidraulica = value_balance(hidraulica)
    p_eolica = value_balance(eolica)
    p_hidroeolica = value_balance(hidroeolica)
    p_fotovoltaica = value_balance(fotovoltaica)
    p_termica = value_balance(termica)
    p_otras = value_balance(otras)
    p_residuos = value_balance(residuos)

    data = [p_hidraulica, p_eolica, p_hidroeolica, p_fotovoltaica, p_termica, p_otras, p_residuos]
    names = ["Hidráulica","Eólica","Hidroeólica","Solar fotovoltaica","Solar térmica","Otras renovables","Residuos renovables"]
    colors = ["#F34213","#2E2E3A","#DE9151","#BC5D2E","#BBB8B2","#913827","#754634"]
    desfase = (0, 0, 0, 0, 0, 0, 0)

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors, explode=desfase)
    plt.axis("equal")
    plt.show()

def co2_no_renewable(inicio, fin):
    
    start = datetime.datetime(int(START_YEAR), int(inicio), 1, 0, 0, 0)
    end = datetime.datetime(int(END_YEAR), int(fin), 1, 0, 0, 0)

    carbon = my_col2.find({"type":"co2_no_renewable", "resource_type":"Carbón", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    diesel = my_col2.find({"type":"co2_no_renewable", "resource_type":"Motores diésel", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    gas = my_col2.find({"type":"co2_no_renewable", "resource_type":"Turbina de gas", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    vapor = my_col2.find({"type":"co2_no_renewable", "resource_type":"Turbina de vapor", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    ciclo = my_col2.find({"type":"co2_no_renewable", "resource_type":"Ciclo combinado", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    congeneracion = my_col2.find({"type":"co2_no_renewable", "resource_type":"Cogeneración", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    residuos = my_col2.find({"type":"co2_no_renewable", "resource_type":"Residuos no renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")

    p_carbon = value_balance(carbon)
    p_diesel = value_balance(diesel)
    p_gas = value_balance(gas)
    p_vapor = value_balance(vapor)
    p_ciclo = value_balance(ciclo)
    p_congeneracion = value_balance(congeneracion)
    p_residuos = value_balance(residuos)

    data = [p_carbon, p_diesel, p_gas, p_vapor, p_ciclo, p_congeneracion, p_residuos]
    names = ["Carbón","Motores diésel","Turbina de gas","Turbina de vapor","Ciclo combinado","Cogeneración","Residuos no renovables"]
    colors = ["#F34213","#2E2E3A","#DE9151","#BC5D2E","#BBB8B2","#913827","#754634"]
    desfase = (0, 0.1, 0.3, 0, 0, 0, 0)

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors, explode=desfase)
    plt.axis("equal")
    plt.show()

def demand_price_market():

    start = datetime.datetime(int(START_YEAR), 1, 1, 0, 0, 0)
    end = datetime.datetime(int(END_YEAR), 12, 31, 0, 0, 0)

    demand = value_per_month("demand")
    price = value_per_month("price_market")

    fig = plt.figure() 
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    xx = range(len(demand))
    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

    
    ax1.bar(xx, demand, width=0.4, label="Demanda", color="#F34213", align='center')
    ax1.set_xticks(xx)
    ax1.set_xticklabels(meses)
    ax1.set_ylabel("Demanda")

    ax2.bar(xx, price, width=0.4, label="Precio de Mercado", color="#2E2E3A", align='center')
    ax2.set_xticks(xx)
    ax2.set_xticklabels(meses)
    ax2.set_ylabel("Precio de Mercado")

    plt.show()




def value_per_month(aux):

    mes = 1
    average = []

    for a in range(1,13):

        start = datetime.datetime(int(START_YEAR), int(mes), 1, 0, 0, 0)
        end = datetime.datetime(int(END_YEAR), int(mes), int(days_in_month(mes)), 0, 0, 0)

        y = 0

        if str(aux) == "demand":

            for x in my_col3.find({"type":str(aux), "datetime": {'$lt': end, '$gte': start}}).distinct("value"):

                y = y + int(x)
        
        elif str(aux) == "price_market":

            for x in my_col4.find({"type":str(aux), "datetime": {'$lt': end, '$gte': start}}).distinct("value"):

                y = y + int(x)

        average.append(y)
        mes = mes + 1
    
    return average

    

def month(x):

    if x==1:
        return "Enero"
    elif x==2:
        return "Febrero"
    elif x==3:
        return "Marzo"
    elif x==4:
        return "Abril"
    elif x==5:
        return "Mayo"
    elif x==6:
        return "Junio"
    elif x==7:
        return "Julio"
    elif x==8:
        return "Agosto"
    elif x==9:
        return "Septiembre"
    elif x==10:
        return "Octubre"
    elif x==11:
        return "Noviembre"
    elif x==12:
        return "Diciembre" 

def days_in_month(x):

    if x==1:
        return 31
    elif x==2:
        return 29
    elif x==3:
        return 31
    elif x==4:
        return 30
    elif x==5:
        return 31
    elif x==6:
        return 30
    elif x==7:
        return 31
    elif x==8:
        return 31
    elif x==9:
        return 30
    elif x==10:
        return 31
    elif x==11:
        return 30
    elif x==12:
        return 31 

def main():

    print("\n############################################################")
    print("\nREData with MongoDB")
    print("\n############################################################\n\n")

    print("Introduzca mes de inicio:")
    inicio = input()
    print("Introduzca mes de inicio:")
    fin = input()

    if int(inicio) > 12 or int(fin) > 12 or int(inicio) < 1 or int(fin) < 1:
        print("Datos introducidos no validos\n")
        exit()

    i = month(int(inicio))
    f = month(int(fin))

    print("\n############################################################")
    print("\nConsultas sobre los datos de " + i + " a " + f)
    print("\n############################################################\n\n")

    by_principal_type(inicio, fin)
    by_child_type_renovable(inicio, fin)
    by_child_type_no_renovable(inicio, fin)
    co2_no_renewable(inicio, fin)
    demand_price_market()

main()