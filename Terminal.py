from ANN import MMnorm, MMdenorm
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np

# Extraction et inversion des données:
Open,High,Low,Close,Volume = np.loadtxt('D:\\Domanis\\GitHub\\Newtech-Nexus\\aapl.csv', delimiter=',', skiprows=1, usecols=(1,2,3,4,5),unpack=True)
Open,High,Low,Close,Volume = Open[::-1],High[::-1],Low[::-1],Close[::-1],Volume[::-1]

# Normalisation et regroupement des données:
Datas_Norm = []
for i in range(len(Open)):
	Datas_Norm.append([MMnorm(Open[i],min(Open),max(Open))
	,MMnorm(High[i],min(High),max(High))
	,MMnorm(Low[i],min(Low),max(Low))
	,MMnorm(Close[i],min(Close),max(Close))
	,MMnorm(Volume[i],min(Volume),max(Volume))])
Datas_Norm = np.array(Datas_Norm)

# Séparation des données d'entraînement et de test:
ratio = 0.6
split = int(ratio*len(Datas_Norm))
trainX = Datas_Norm[:split-1]
trainY = Datas_Norm[1:split]
trainOpen = Open[:split-1]
testX = Datas_Norm[split-1:-1]
testY = Datas_Norm[split:]
testOpen = Open[split-1:-1]

# Construction du réseau keras:
np.random.seed(10)
from keras import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import RMSprop
from time import sleep
NET = Sequential()
NET.add(Dense(50,activation='relu',input_shape = (5,)))
NET.add(Dense(5,activation='relu'))
NET.compile(loss='mse',optimizer=RMSprop(lr=0.01))
NET.fit(trainX,trainY,epochs=1000,)

# Prédiction:
Trainp = NET.predict(trainX)[:,0]
Testp = NET.predict(testX)
for i in range(200):
	Testp = np.vstack((Testp,NET.predict(Testp[-1:])))
Testp = Testp[:,0]

# Dénormanisaton:
for i in range(len(Trainp)):
	Trainp[i] = MMdenorm(Trainp[i],min(Open),max(Open))
for i in range(len(Testp)):
	Testp[i] = MMdenorm(Testp[i],min(Open),max(Open))

# Affichage des graphiques:
from GRAPH import *

Traingraph = graphique(titre='Données d\'entraînement',x=range(len(trainOpen)),y=trainOpen,legende='Valeur réelle')
Traingraph.courbe(x=range(len(Trainp)),y=Trainp,legende='Valeur prédite')

Testgraph = graphique(titre='Données de test',x=range(len(testOpen)),y=testOpen,legende='Valeur réelle')
Testgraph.courbe(x=range(len(Testp)),y=Testp,legende='Valeur prédite')


# Comparaison avec l'ancien modèle:
from ANN import *
NET = ExtremeANN(5,50,5)
NET.apprentissage(10000,0.001,trainX,trainY)
Trainp = NET.propagation(trainX)[:,0]
Testp = NET.propagation(testX)
for i in range(200):
	Testp = np.vstack((Testp,NET.propagation(Testp[-1:])))
Testp = Testp[:,0]

for i in range(len(Trainp)):
	Trainp[i] = MMdenorm(Trainp[i],min(Open),max(Open))
for i in range(len(Testp)):
	Testp[i] = MMdenorm(Testp[i],min(Open),max(Open))

Traingraph2 = graphique(titre='Données d\'entraînement 2',x=range(len(trainOpen)),y=trainOpen,legende='Valeur réelle')
Traingraph2.courbe(x=range(len(Trainp)),y=Trainp,legende='Valeur prédite')

Testgraph2 = graphique(titre='Données de test 2',x=range(len(testOpen)),y=testOpen,legende='Valeur réelle')
Testgraph2.courbe(x=range(len(Testp)),y=Testp,legende='Valeur prédite')

plt.show()