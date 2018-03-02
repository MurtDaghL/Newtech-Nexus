with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_2a PRE ALPHA\\ANN.py","r") as script:
		exec(script.read())
import matplotlib, csv
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt, tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Extraction et inversion des données:
Open,High,Low,Close,Volume = np.loadtxt('D:\\Domanis\\PYTHON\\Datas\\aapl.csv', delimiter=',', skiprows=1, usecols=(1,2,3,4,5),unpack=True)
Open,High,Low,Close,Volume = Open[::-1],High[::-1],Low[::-1],Close[::-1],Volume[::-1]
# Création des graphiques matplotlib:
with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_2a PRE ALPHA\\GRAPH.py","r") as script:
	exec(script.read())
Openp = []
Highp = []
Lowp = []
Closep = []
Volumep = []
Openg = graphique(titre='Open',x=range(len(Open)),y=Open,legende='Valeur réelle')
Openg.courbe(x=range(len(Openp)),y=Openp,legende='Valeur prédite')
Highg = graphique(titre='High',x=range(len(High)),y=High,legende='Valeur réelle')
Highg.courbe(x=range(len(Highp)),y=Highp,legende='Valeur prédite')
Lowg = graphique(titre='Low',x=range(len(Low)),y=Low,legende='Valeur réelle')
Lowg.courbe(x=range(len(Lowp)),y=Lowp,legende='Valeur prédite')
Closeg = graphique(titre='Close',x=range(len(Close)),y=Close,legende='Valeur réelle')
Closeg.courbe(x=range(len(Closep)),y=Closep,legende='Valeur prédite')
Volumeg = graphique(titre='Volume',x=range(len(Volume)),y=Volume,legende='Valeur réelle')
Volumeg.courbe(x=range(len(Volumep)),y=Volumep,legende='Valeur prédite')

# Normalisation et regroupement des données:
Datas_Norm = []
for i in range(len(Open)):
	Datas_Norm.append([norm(Open[i],min(Open),max(Open))
	,norm(High[i],min(High),max(High))
	,norm(Low[i],min(Low),max(Low))
	,norm(Close[i],min(Close),max(Close))
	,norm(Volume[i],min(Volume),max(Volume))])
# Suppressions de données pour l'entrainement:
Attendu = Datas_Norm
for i in range(20):
	del Attendu[len(Attendu)-1]
Input = Attendu
del Input[len(Input)-1]

# Affichage de la fenêtre tkinter
with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_2a PRE ALPHA\\GUI.py","r") as script:
		exec(script.read())

# Affiche performance optimale:
N,E,T,Err_moy = np.loadtxt("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\Historique.csv", delimiter = ',', skiprows=1 , usecols=(0,1,2,4),unpack=True)
index = list(Err_moy).index(min(Err_moy))

afficher('D\'après l\'historique, voici les paramètres optimaux:')
afficher('Nombre de neurones: {N}'.format(N=N[index]))
afficher('Nombre d\'essais: {E}'.format(E=E[index]))
afficher('Taux d\'apprentissage: {T}'.format(T=T[index]))
afficher('Erreur moyenne: {Err}'.format(Err=Err_moy[index]))
afficher('\n \n \n \n \n')
afficher('Veuillez rentrer vos paramètres\n')
fenetre.mainloop()