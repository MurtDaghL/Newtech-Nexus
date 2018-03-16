from ANN import *
from GRAPH import *
import matplotlib
import matplotlib.pyplot as plt, numpy as np
from time import sleep, time

"""IMPORTATION ET TRAITEMENT DES DONNEES:"""

	# Extraction et inversion des données:
Open,High,Low,Close,Volume = np.loadtxt('D:\\Domanis\\GitHub\\Newtech-Nexus\\aapl.csv', delimiter=',', skiprows=1, usecols=(1,2,3,4,5),unpack=True)
Open,High,Low,Close,Volume = Open[::-1],High[::-1],Low[::-1],Close[::-1],Volume[::-1]

	# Normalisation et regroupement des données en séquences de 5 jours:
Sequence = []
Datas = []
taille_sequence = 5
dimension = 5

debut = time()
i = 0
while i < len(Open):
	Open_norm = MMnorm(Open[i],min(Open),max(Open))
	High_norm = MMnorm(High[i],min(High),max(High))
	Low_norm = MMnorm(Low[i],min(Low),max(Low))
	Close_norm = MMnorm(Close[i],min(Close),max(Close))
	Volume_norm = MMnorm(Volume[i],min(Volume),max(Volume))
	Sequence.append([Open_norm,High_norm,Low_norm,Close_norm,Volume_norm])
	i += 1
	if len(Sequence) == taille_sequence:
		Datas.append(Sequence)
		i -= taille_sequence-1  # Utile pour que les séquences soient décalés les unes des autres de un jour uniquement 
		Sequence = []
	
fin = time()
Datas = np.array(Datas)
print("EXTRACTION ET NORMALISATION TERMINEE, durée: {temps}\nDimensions du tenseur de données: {dim} ".format(temps=fin-debut,dim=Datas.shape))

	# Séparation des données d'entraînement et de test:
ratio = 1
split = int(ratio*len(Datas))
trainX = Datas[:split-1] #Entrée donnée au réseau, correspond à une séquence de 5 jours
trainY = Datas[1:split,0,0] #Prédiction attendue, correspond à la valeur Open du jour suivant la séquence
testX = Datas[split-1:-1]
testY = Datas[split:,0,0]



"""CREATION ET UTILISATION DU RESEAU NEURONAL:"""

	# Construction du réseau keras:
from keras import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import RMSprop
np.random.seed(10)

debut = time()
NET = Sequential()
NET.add(LSTM(1, activation='relu', input_shape=(taille_sequence,dimension)))
# NET.add(LSTM(5,activation='relu'))
NET.compile(loss='mse',optimizer=RMSprop(lr=0.01))
fin = time()
print("COMPILATION TERMINEE, Durée: "+ str(fin-debut))

	# Visualisation du réseau créé:
from keras.utils import plot_model
# plot_model(NET,'model.png')

	# Apprentissage du réseau:
debut = time()
NET.fit(trainX,trainY,epochs=1000,validation_split=0.6)
fin = time()
print("APPRENTISSAGE TERMINE, Durée: "+ str(fin-debut))

	# Prédiction:
Predict = NET.predict(trainX)
# for i in range(100):
# 	Predict.append(NET.predict(Predict[-1]))

	# Dénormanisaton des prédictions:
for i in range(len(Predict)):
	Predict[i] = MMdenorm(Predict[i],min(Open),max(Open))

	# Affichage des graphiques:
trainOpen = Open[:split-1]
Predictgraph = graphique(titre='Valeur, à l\'ouverture, de l\'action Apple',x=range(len(trainOpen)),y=trainOpen,legende='Valeur réelle')
Predictgraph.courbe(x=range(len(Predict)),y=Predict,legende='Valeur prédite')

"""COMPARAISON AVEC L'ANCIEN MODELE:"""

# NET = ExtremeANN(5,50,5)
# NET.apprentissage(10000,0.001,trainX,trainY)
# Trainp = NET.propagation(trainX)[:,0]
# Testp = NET.propagation(testX)
# for i in range(200):
# 	Testp = np.vstack((Testp,NET.propagation(Testp[-1:])))
# Testp = Testp[:,0]

	# Dénormanisaton des prédictions:
# for i in range(len(Trainp)):
# 	Trainp[i] = MMdenorm(Trainp[i],min(Open),max(Open))
# for i in range(len(Testp)):
# 	Testp[i] = MMdenorm(Testp[i],min(Open),max(Open))

	# Affichage des graphiques:
# Traingraph2 = graphique(titre='Données d\'entraînement 2',x=range(len(trainOpen)),y=trainOpen,legende='Valeur réelle')
# Traingraph2.courbe(x=range(len(Trainp)),y=Trainp,legende='Valeur prédite')

# Testgraph2 = graphique(titre='Données de test 2',x=range(len(testOpen)),y=testOpen,legende='Valeur réelle')
# Testgraph2.courbe(x=range(len(Testp)),y=Testp,legende='Valeur prédite')

plt.show()