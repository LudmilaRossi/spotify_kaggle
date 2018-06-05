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

pred_train=lm.predict(X_train)
pred_test=lm.predict(X_test)

print('LINEAR MODEL')
print ("Fit a model X_train, and calculate MSE with Y_train:", np.mean((Y_train - lm.predict(X_train)) ** 2))
print ("Fit a model X_train, and calculate MSE with X_test, Y_test:",     np.mean((Y_test - lm.predict(X_test)) ** 2))



model_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
model_rbf.fit(X_train, Y_train)
print(50*'-')
print('RBF MODEL')
print ("Fit a model X_train, and calculate MSE with Y_train:", np.mean((Y_train - model_rbf.predict(X_train)) ** 2))
print ("Fit a model X_train, and calculate MSE with X_test, Y_test:", np.mean((Y_test - model_rbf.predict(X_test)) ** 2))



plt.scatter(lm.predict(X_train), lm.predict(X_train)-Y_train, color='b', s=40, alpha=0.5, marker='.')
plt.scatter(lm.predict(X_test), lm.predict(X_test)-Y_test, color='g', s=40, marker='.')
plt.hlines(y=0,xmin=-10, xmax=60, color='r')
plt.title('Lineal Model- Residual Plot using training (blue) and test (green) data')
plt.ylabel('Residuals')
plt.show()

plt.scatter(model_rbf.predict(X_train), model_rbf.predict(X_train)-Y_train,     color='b', s=40, alpha=0.5, marker='.')
plt.scatter(model_rbf.predict(X_test), model_rbf.predict(X_test)-Y_test, color='g', s=40, marker='.')
plt.hlines(y=0,xmin=0, xmax=70, color='r')
plt.title('RBF Model - Residual Plot using training (blue) and test (green) data')
plt.ylabel('Residuals')
