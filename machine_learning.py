## Predecir la posición de una canción del ranking de Spotify
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

#read csv
sp=pd.read_csv('data.csv', sep=',')

sp.columns=['position','track_name','artist','streams','url','date','region']  ##renombro columnas por comodidad

paises={'es':'España','it':'Italia','cy':'Cipre','ar':'Argentina','al':'Albania',
    'at':'Austria','au':'Australia','be':'Belgica','bo':'Bolivia','br':'Brasil',
    'ca':'Canada','ch':'Suiza','cl':'Chile','co':'Colombia','cr':'Costa Rica',
    'cz':'Republica Checa','de':'Alemania','dk':'Dinamarca','do':'Republica Dominicana',
    'ec':'Ecuador','ee':'Estonia','es':'España','fi':'Finlandia','fr':'Francia',
    'gb':'Gran Bretaña','gr':'Grecia','gt':'Guatemala','hk':'Hong Kong','hn':'Honduras',
    'hu':'Hungria','id':'Indonesia','ie':'Irlanda','is':'Islandia','jp':'Japon','lt':'Lituania',
    'lv':'Letonia','mx':'Mexico','my':'Malasia','nl':'Paises Bajos','no':'Noruega',
    'nz':'Neva Zelanda','pa':'Panama','pe':'Peru', 'ph':'Filipinas', 'pl':'Polonia',
    'pt':'Portugal','py':'Paraguay','se':'Suecia','sg':'Singapur','sk':'Eslovaquia',
    'sv':'El Salvador','tr':'Turquia','tw':'Taiwan','us':'Estados Unidos','uy':'Uruguay','global':'Global'} ##completar el diccionario

#Listado de canciones
songs=sp.track_name.unique()
songs=songs.tolist()

#Como obternet el array countries
#aux=sp.groupby('region').sum().reset_index()
#aux=aux.region.tolist()
countries = ['ar','at','au','be','bo','br','ca','ch','cl','co','cr','cy','cz','de','dk',
 'do','ec','ee','es','fi','fr','gb','global','gr','gt','hk','hn','hu','id','ie','is','it','jp','lt','lv',
 'mx','my','nl','no','nz','pa','pe','ph','pl','pt','py','se','sg','sk','sv','tr','tw','us','uy']


##### Esta funcion permite ver los streams max y min a segunda de la agrupacion
def maxMin(df, gb, mercado):    #df=Dataframe    gb=modo de grupby

    if mercado!=None:
        df=df[df.region==mercado]
        titulo=paises.get(mercado)
        print('--------------',titulo.upper(),'--------------')
    elif mercado==None:
        print('--------------MUNDO--------------')

    df=df.groupby(gb).sum().reset_index()
    df=df.drop('position', 1)
    df=df[df[gb]!='global']

   # print(df)

    print('MAX')
    maxx=df[df.streams==df.streams.max()]
    print(gb,' : ',maxx.iloc[0,0])
    print('streams : ',maxx.iloc[0,1])

    print(30*'-')
    print('MIN')
    minn=df[df.streams==df.streams.min()]
    print(gb,' : ',minn.iloc[0,0])
    print('streams : ',minn.iloc[0,1])


def weeksInTop(df, song, top, country):

    df=df[df.region==country]
    df=df[df.track_name==song]
    df=df[df.position<=top]
    fecha_inicio=datetime.strptime(df.date.min(), '%Y-%m-%d')
    fecha_fin=datetime.strptime(df.date.max(), '%Y-%m-%d')

    date_delta=fecha_fin-fecha_inicio
    weeks=date_delta.days/7.0
    return int(weeks)

def Top(df, top, country, date):
    df=df[df.region==country]
    df=df[df.position<=top]
    df=df[df.date==date]

    return df

def scatterPlot(df, song, country):
    df=sp[sp.region==country]
    df=df[df.track_name==song]
    df.date = pd.to_datetime(df.date) # convert the date column to Datetime

    fig, ax = plt.subplots()
    ax.scatter([x for x in df.date], df.position, marker=".")
    fig.autofmt_xdate()
    myFmt = DateFormatter("%m")
    ax.xaxis.set_major_formatter(myFmt)
    plt.xlim('2017-01-01', '2017-09-1')
    plt.title(song.upper())
    plt.xlabel('Meses')
    plt.ylabel('Posiciones')
    plt.show()


def TopCountry(df, top, country, date):
    top_c=Top(sp , top , country, date)
    top_c=top_c.track_name
    top_c=top_c.to_frame()
    top_c.columns=[country]
    top_c=top_c.reset_index()
    top_c=top_c.drop('index', 1)
    return top_c


def TopWorld(df, top , date, countries=[]):
    top_mundial=pd.DataFrame()

    for i in range(0, len(countries)):
        top_country=TopCountry(sp, top, countries[i], date)
        top_mundial=pd.concat([top_mundial, top_country], axis=1)


    return top_mundial


def Matrix4Corr(df, top, date, countries=[]):
    arr_top=[]
    vacios=[]

    for i in range(0, len(countries)):
        top_country=TopCountry(sp, top, countries[i], date)
        top_country=top_country[countries[i]].values
        top_country=tuple(top_country)
        if not top_country:
            vacios.append(countries[i])
        arr_top.append(top_country)

    matrix=pd.Series(arr_top).apply(frozenset).to_frame(name='top')

    for top in frozenset.union(*matrix.top):
        matrix[top] = matrix.apply(lambda _: int(top in _.top), axis=1)


    matrix.index=countries
    matrix=matrix.drop('top', 1)
    for i in range(0, len(vacios)):
        matrix=matrix.drop(vacios[i],0)

    matrix=matrix.transpose()


    return matrix

def betterCorr(x):
    if x>0:
        1-x
    else:
        1+x


#para el mercado mundial
#maxMin(sp,'region',None)   ### track_name, artist, region, date

####Para solo el mercado español
#maxMin(sp,'artist','es')

song='Shape of You'
top=20
country='es'
date='2017-01-01'  ###2017-03-01 existen nans

####TOP por fecha y pais

#a=Top(sp , top , country, date)
#print(song,'-','Semanas en Top',top,' : ', weeksInTop(sp, song, top, country))

#### SCATTERPLOT
#scatterPlot(sp, song, country)

#Lista de canciones Top en un cierto pais

#print(TopCountry(sp, top, country, date))

#Big DataFrame tops por pais
#a=TopWorld(sp, top, date, countries)  ## si hay nan en registros es porque no hay datos en esa fecha


"""
europa=['es','it','fr','gr','al','cy','be','ch','cz','de','dk','ee','fi','gb','hu','ie','is',
    'lt','lv','nl','no','pl','pt','se','sk','tr']

america=['ar','bo','cl','co','cr','do','ec','gt','hn','mx','pa','pe','py','sv','us','uy']

lejos=['es','ar','it','jp','id','au','us']
mat=Matrix4Corr(sp, 5, '2017-01-01', lejos)


corr = mat.corr()

import seaborn as sns
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)

"""
