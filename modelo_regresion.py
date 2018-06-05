#1st January 2017 to 17th August 2017
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR


# Load CSV and columns
sp=pd.read_csv('data.csv', sep=',')

sp.columns=['position','track_name','artist','streams','url','date','region'] 

song='Chantaje'
country='es'


df=sp[sp.region==country]
df=df[df.track_name==song]

df.date = pd.to_datetime(df.date) # convert the date column to Datetime
df.date=df['date'].apply(lambda x: x.toordinal())

X = df['date'].values[:,np.newaxis]  

y = df['position'].values

fig, ax = plt.subplots()
ax.scatter(X, y, color='darkorange', marker='.')

fig.autofmt_xdate()
myFmt = DateFormatter("%m")
ax.xaxis.set_major_formatter(myFmt)



lm = LinearRegression()

lm.fit(X, y)

plt.plot(X, lm.predict(X),color='r', label='Linear Model')



fecha='2017-08-18'   ###fecha prediccion
fecha_predict=fecha
fecha_predict=pd.to_datetime(fecha_predict)
fecha_predict=fecha_predict.toordinal()
X_predict = fecha_predict # put the dates of which you want to predict
y_predict = lm.predict(X_predict)
print('Linear Model - ',fecha, song,'Posicion : ',int(y_predict))

mse_lineal=np.mean((y-lm.predict(X))**2)
print('Error cuadratico medio',mse_lineal)

#prediccion modelo rbf
model_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
model_rbf.fit(X, y)
plt.plot(X, model_rbf.predict(X), color='navy', label='RBF model')
y_rbf_predict=model_rbf.predict(X_predict)
print(50*'-')
print('Non-Linear Model - ',fecha, song,'Posicion : ',int(y_rbf_predict))

mse_rbf=np.mean((y-model_rbf.predict(X))**2)
print('Error cuadratico medio',mse_rbf)

plt.title(song.upper())
plt.xlabel('Meses')
plt.ylabel('Posiciones')

plt.show()

plt.scatter(y, lm.predict(X), marker='.') 
plt.scatter(y, model_rbf.predict(X), marker='.') 
plt.xlabel('Posiciones')
plt.ylabel('Posiciones estimadas')
