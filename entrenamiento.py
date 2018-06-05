import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import sklearn
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

#### dividir el data sert randomicamente entre train y test
X_train, X_test, Y_train, Y_test=sklearn.cross_validation.train_test_split(
        X, y, test_size=0.33, random_state=5)




lm = LinearRegression()
lm.fit(X_train, Y_train)
