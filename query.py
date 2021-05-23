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

    start = datetime.datetime(int(year), int(inicio), 1, 0, 0, 0)
    end = datetime.datetime(int(year), int(fin), 1, 0, 0, 0)
    
    renewable = my_col.find({"principal_type":"Renovable", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    no_renewable = my_col.find({"principal_type":"No-Renovable", "datetime": {'$lt':end, '$gte':start}}).distinct("value")

    p_renewable = value_balance(renewable)
    p_no_renewable = value_balance(no_renewable)

    data = [p_renewable, p_no_renewable]
    names = ["Renobable","No Renobable"]
    colors = ["#F34213","#2E2E3A"]
    
    #SEPARATED PIECE
    offset = (0, 0.1)

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors, explode=offset)
    plt.axis("equal")
    plt.show()



def value_balance(collection):
    y = 0 
    for x in collection:
        y = y + int(x)
    return y



def by_child_type_no_renovable(year, inicio, fin):

    start = datetime.datetime(int(year), int(inicio), 1, 0, 0, 0)
    end = datetime.datetime(int(year), int(fin), 1, 0, 0, 0)

    congeneracion = my_col.find({ "principal_type":"No-Renovable", "child_type":"Cogeneración", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    vapor = my_col.find({ "principal_type":"No-Renovable", "child_type":"Turbina de vapor", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    bombeo = my_col.find({ "principal_type":"No-Renovable", "child_type":"Turbinación bombeo", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    nuclear = my_col.find({ "principal_type":"No-Renovable", "child_type":"Nuclear", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    ciclo = my_col.find({ "principal_type":"No-Renovable", "child_type":"Ciclo combinado", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    carbon = my_col.find({ "principal_type":"No-Renovable", "child_type":"Carbón", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    diesel = my_col.find({ "principal_type":"No-Renovable", "child_type":"Motores diésel", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    gas = my_col.find({ "principal_type":"No-Renovable", "child_type":"Turbina de gas", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    residuos = my_col.find({ "principal_type":"No-Renovable", "child_type":"Residuos no renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")

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
    offset = (0, 0.2, 0, 0, 0, 0, 0, 0.2, 0)

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors, explode=offset)
    plt.axis("equal")
    plt.show()



def by_child_type_renovable(year, inicio, fin):

    start = datetime.datetime(int(year), int(inicio), 1, 0, 0, 0)
    end = datetime.datetime(int(year), int(fin), 1, 0, 0, 0)

    hidraulica = my_col.find({ "principal_type":"Renovable", "child_type":"Hidráulica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    eolica = my_col.find({ "principal_type":"Renovable", "child_type":"Eólica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    hidroeolica = my_col.find({ "principal_type":"Renovable", "child_type":"Hidroeólica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    fotovoltaica = my_col.find({ "principal_type":"Renovable", "child_type":"Solar fotovoltaica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    termica = my_col.find({ "principal_type":"Renovable", "child_type":"Solar térmica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    otras = my_col.find({ "principal_type":"Renovable", "child_type":"Otras renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    residuos = my_col.find({ "principal_type":"Renovable", "child_type":"Residuos renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")

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



def by_child_type_renovable(year, inicio, fin):

    start = datetime.datetime(int(year), int(inicio), 1, 0, 0, 0)
    end = datetime.datetime(int(year), int(fin), 1, 0, 0, 0)

    hidraulica = my_col.find({ "principal_type":"Renovable", "child_type":"Hidráulica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    eolica = my_col.find({ "principal_type":"Renovable", "child_type":"Eólica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    hidroeolica = my_col.find({ "principal_type":"Renovable", "child_type":"Hidroeólica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    fotovoltaica = my_col.find({ "principal_type":"Renovable", "child_type":"Solar fotovoltaica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    termica = my_col.find({ "principal_type":"Renovable", "child_type":"Solar térmica", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    otras = my_col.find({ "principal_type":"Renovable", "child_type":"Otras renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    residuos = my_col.find({ "principal_type":"Renovable", "child_type":"Residuos renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")

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
    offset = (0, 0, 0, 0, 0, 0, 0)

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors, explode=offset)
    plt.axis("equal")
    plt.show()



def co2_no_renewable(year, inicio, fin):

    start = datetime.datetime(int(year), int(inicio), 1, 0, 0, 0)
    end = datetime.datetime(int(year), int(fin), 1, 0, 0, 0)

    carbon = my_col2.find({"resource_type":"Carbón", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    diesel = my_col2.find({"resource_type":"Motores diésel", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    gas = my_col2.find({"resource_type":"Turbina de gas", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    vapor = my_col2.find({"resource_type":"Turbina de vapor", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    ciclo = my_col2.find({"resource_type":"Ciclo combinado", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    congeneracion = my_col2.find({"resource_type":"Cogeneración", "datetime": {'$lt': end, '$gte': start}}).distinct("value")
    residuos = my_col2.find({"resource_type":"Residuos no renovables", "datetime": {'$lt': end, '$gte': start}}).distinct("value")

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
    offset = (0, 0.1, 0.3, 0, 0, 0, 0)

    plt.pie(data, labels=names, autopct="%0.1f %%", colors=colors, explode=offset)
    plt.axis("equal")
    plt.show()



def demand_price_market(year):
    demand = value_per_month("demand", year)
    price = value_per_month("price_market", year)

    plt.figure() 
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



def value_per_month(aux,year):
    average = []

    for month in range(1,13):
        start = datetime.datetime(int(year), int(month), 1, 0, 0, 0)
        end = datetime.datetime(int(year), int(month), int(monthrange(year, month)[1]), 0, 0, 0)
        y = 0

        if str(aux) == "demand":
            for x in my_col3.find({"type":str(aux), "datetime": {'$lt': end, '$gte': start}}).distinct("value"):
                y = y + int(x)
        
        elif str(aux) == "price_market":
            for x in my_col4.find({"type":str(aux), "datetime": {'$lt': end, '$gte': start}}).distinct("value"):
                y = y + int(x)

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

    if start_month>=end_month or start_month>=12 or end_month>=12 or start_month<0 or end_month<0 or year<0 or this_year<year or (this_year==year and (this_month<=start_month or this_month<=end_month)):
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

    by_principal_type(year, start_month, end_month)
    by_child_type_renovable(year, start_month, end_month)
    by_child_type_no_renovable(year, start_month, end_month)
    co2_no_renewable(year, start_month, end_month)
    demand_price_market(year)
