import requests
import datetime
import pandas as pd

__headers = {
        'x-rapidapi-key': "9c4262a1a4msh005d4aa2c90e1f8p1db426jsnca9f76572a55",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }

#Entrada de datos, aqui se procesa cada una de las series del fichero que contiene el listado de series. Obteniendo los atributos, luego se llama a la funcion output_data para exportar.
def input_data():
    cont=0
    data =[]
    with open("series.txt", "r", encoding="UTF-8") as series:
        for serie in series:
            serie = serie.replace("\n","")
            print("Processing " + serie+"...")
            data.append(get_caps(serie) + get_ratings(serie))
            output_data(data,cont)
            cont+=1
        series.close()
        print("Completed")

#Aqui se exporta la informacion en un fichero xlsx .
def output_data(data,startrow):

    series = {}
    df = pd.DataFrame(series, columns=['Nombre', 'Duración', 'Año', 'Rank_IDBM', 'Rating_IDBM','NºTemporadas', 'NºCaps'])
    for serie in data:

#Control de errores de incompatibilidad en la busqueda
        if serie[0] != serie[1]:
            with open("errores.txt", "w+", encoding="UTF-8") as errores:
                errores.write('{0} {1}\n'.format(serie[0], serie[1]))
            errores.close()
            print("Hay errores")
        else:#Dataframe a exportar
            df = df.append({'Nombre': serie[0],
                    'Duración': serie[2],
                    'Año': serie[5],
                    'Rank_IDBM':serie[6],
                    'Rating_IDBM':serie[7],
                    'NºTemporadas': serie[3],
                    'NºCaps':serie[8]
                    },ignore_index=True)

            #Se almacenan los min de la serie entera para luego obtener el total en en formato correcto.
            with open("temp.txt", "a+", encoding="UTF-8") as temp:
                temp.write(str(serie[4]))
                temp.write('\n')
            temp.close()

#Exportacion del dataframe en archivo xlsx
    df.to_excel(r'Series_procesadas.xlsx', startrow=startrow, index=False, header=True)

#Se obtiene el id la serie, el nombre de lo que se encontro y el tipo de programa.
def get_id(name):

    url = "https://imdb8.p.rapidapi.com/title/auto-complete"
    querystring = {"q": name,"currentCountry":"ES"}
    response = requests.request("GET", url, headers=__headers, params=querystring)
    resp = response.json()

    try:
        id = resp["d"][0]["id"]
        nombre = resp["d"][0]["l"]
        type = resp["d"][0]["q"]
    except KeyError:
        print("Error, id no encontrado ",name)

    return id,nombre,type

#Se obtiene el año , ratings, rank en imdb y nº de episodios
def get_ratings(name):
    url = "https://imdb8.p.rapidapi.com/title/get-overview-details"
    querystring = {"tconst": get_id(name)}
    response = requests.request("GET", url, headers=__headers, params=querystring)
    resp = response.json()
    try:
        year = resp["title"]["year"]
        numberOfEpisodes = resp["title"]["numberOfEpisodes"]
        rating_idbm = resp["ratings"]["rating"]
        rank_idbm = resp["ratings"]["otherRanks"][0]["rank"]

    except KeyError:
        print("Error, año,number,rating o rank no encontrados")
        pass
    return year,rank_idbm,rating_idbm,numberOfEpisodes

#Aqui se obtiene la informacion de la serie general y se procesa uno a uno cada episodio
def get_caps(name):

    url = "https://imdb8.p.rapidapi.com/title/get-seasons"
    querystring = {"tconst":get_id(name)[0],"currentCountry":"ES"}
    response = requests.request("GET", url, headers=__headers, params=querystring)
    try:
        resp = response.json()
    except KeyError:
        pass

    episodes = []
    times = []
    seasons = len(resp)
    for i in range(len(resp)):
        episodes.extend(resp[i]["episodes"])
    for episode in episodes:
        id_ep = str(episode["id"])
        id_ep = id_ep.replace("title", "").replace("/","")
        try:
            times.append(get_time(id_ep))
        except ValueError:
            pass
#Se devuelve el nombre inciial , el nombre encontrado, el tiempo total de la serie en formato, nº de seasons, y en min el tiempo total de la serie
    return name,get_id(name)[1],get_totalTimeFormat(times),seasons,sum(times)

#Se obtiene el tiempo en min de un capitulo
def get_time(id_ep):

    url = "https://imdb8.p.rapidapi.com/title/get-details"
    querystring = {"tconst":id_ep,"currentCountry":"ES"}
    response = requests.request("GET", url, headers=__headers, params=querystring)
    try:
        print(response.text)
        resp = response.json()
        time_in_minutes = resp["runningTimeInMinutes"]
    except KeyError:
        pass
    return time_in_minutes

#Se suman todos los tiempos de los capitulos y se devuelve en un formato
def get_totalTimeFormat(times):

    total_time_out = datetime.timedelta(minutes=sum(times))
    return '{} Días, {} Horas y {} minutos.'.format(total_time_out.days, total_time_out.seconds//3600, (total_time_out.seconds//60)%60)

#Inicia el programa
input_data()
