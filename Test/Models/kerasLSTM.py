from ANN import MMnorm, MMdenorm
from GRAPH import *
import matplotlib
import matplotlib.pyplot as plt, numpy as np
from time import sleep, time

"""IMPORTATION ET TRAITEMENT DES DONNEES:"""

	# Extraction et inversion des données:
Open,High,Low,Close,Volume = np.loadtxt('D:\\Domanis\\GitHub\\Newtech-Nexus\\Datas\\aapl.csv', delimiter=',', skiprows=1, usecols=(1,2,3,4,5),unpack=True)
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
print("EXTRACTION ET NORMALISATION TERMINEE, durée: {temps}\nDimensions du tenseur de données: {dim}".format(temps=fin-debut,dim=Datas.shape))


"""CREATION ET UTILISATION DU RESEAU NEURONAL:"""

Input = Datas[:-1] #Entrée donnée au réseau, correspond à une séquence de 5 jours
Attendu = Datas[1:] #Prédiction attendue, la séquence de 5 jours suivante

	# Construction du réseau keras:
from keras import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.optimizers import RMSprop
np.random.seed(10)

debut = time()
NET = Sequential()
NET.add(LSTM(50, activation='relu', input_shape=(taille_sequence,dimension),return_sequences=True))
NET.add(Dropout(0.2))
NET.add(LSTM(100,activation='relu',return_sequences=True))
NET.add(Dropout(0.2))
NET.add(LSTM(5,activation='linear',return_sequences=True))
NET.compile(loss='mse',optimizer=RMSprop(lr=0.001,decay=0.0001))
fin = time()
print("COMPILATION TERMINEE, Durée: "+ str(fin-debut))

	# Visualisation du réseau créé:
from keras.utils import plot_model
plot_model(NET,'D:\\Domanis\\GitHub\\Newtech-Nexus\\Saves\\model.png',show_shapes=True)

	# Apprentissage du réseau:
debut = time()
NET.fit(Input,Attendu,epochs=100,validation_split=0.05)
fin = time()
print("APPRENTISSAGE TERMINE, Durée: "+ str(fin-debut))
NET.save('lstm_model.h5')

	# Prédiction:
Predict = NET.predict(Input[:-155])
for i in range(20):
	Predict = np.vstack((Predict,NET.predict(Predict[-1].reshape((1,taille_sequence,dimension)))))

	# Transformation de la liste de séquences en une unique séquence et supression des doublons:
Predict = list(Predict.reshape((len(Predict)*taille_sequence,dimension))[:,0])

New_Predict = []
for i in range(len(Predict)):
	if i % taille_sequence == 0:
		New_Predict.append(Predict[i])
Predict = New_Predict
del New_Predict

	# Dénormanisaton des prédictions:
for i in range(len(Predict)):
	Predict[i] = MMdenorm(Predict[i],min(Open),max(Open))

	# Affichage des graphiques:
Predictgraph = graphique(titre='Valeur, à l\'ouverture, de l\'action Apple',x=range(len(Open)),y=Open,legende='Valeur réelle')
Predictgraph.courbe(x=range(len(Predict)),y=Predict,legende='Valeur prédite')
plt.show()