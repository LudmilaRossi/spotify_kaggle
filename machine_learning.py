## Predecir la posición de una canción del ranking de Spotify
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