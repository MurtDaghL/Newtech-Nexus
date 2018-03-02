with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_1d PRE ALPHA\\ANN.py","r") as script:
		exec(script.read())
import matplotlib, csv
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt, tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

# Extraction et inversion des données:
Open,High,Low,Close,Volume = np.loadtxt('D:\\Domanis\\PYTHON\\Datas\\aapl.csv', delimiter=',', skiprows=1, usecols=(1,2,3,4,5),unpack=True)
Open,High,Low,Close,Volume = Open[::-1],High[::-1],Low[::-1],Close[::-1],Volume[::-1]

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

# Affiche performance optimale:
N,E,T,Err_moy = np.loadtxt("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\Historique.csv", delimiter = ',', skiprows=1 , usecols=(0,1,2,4),unpack=True)
index = list(Err_moy).index(min(Err_moy))
print('D\'après l\'historique, voici les paramètres optimaux:')
print('Nombre de neurones: ',N[index])
print('Nombre d\'essais: ',E[index])
print('Taux d\'apprentissage:',T[index])
print('Erreur moyenne: ',Err_moy[index])
print('\n \n \n \n \n')

# Entrées utilisateur:
print('Veuillez rentrer vos paramètres\n')
N = int(input('Nombre de neurones de la couche intermediaires: '))
if N > 1000:
	print('C\'est une mauvaise idée')
E = int(input('Nombres d\'essais: '))
if E > 1000000:
	print('Il va falloir être très patient')
T = float(input('Taux d\'apprentissage (taux conseillé < 0.1): '))
input('\nDébut de l\'apprentissage:')

# Définition réseau et apprentissage:
PredictApple = ExtremeANN(5,N,5)
PredictApple.apprentissage(E,T,Input,Attendu)
print('\n \n \n \n \n')
# Prédiction des données supprimées:
z = list(PredictApple.propagation(Input))
for i in range(21):
	z.insert(len(z)-1,PredictApple.propagation(z[len(z)-1]))

# Dénormanisation et séparation:
Openp = []
Highp = []
Lowp = []
Closep = []
Volumep = []
for i in range(len(z)):
	Openp.append(denorm(z[i][0],min(Open),max(Open)))
	Highp.append(denorm(z[i][1],min(High),max(High)))
	Lowp.append(denorm(z[i][2],min(Low),max(Low)))
	Closep.append(denorm(z[i][3],min(Close),max(Close)))
	Volumep.append(denorm(z[i][4],min(Volume),max(Volume)))
	
print('Enregistrement de la performance du réseau')
Erreur = str(PredictApple.quadratique(Input,Attendu))
Erreur_str = Erreur.replace('[','')
Erreur_str = Erreur_str.replace(']','')
Erreur_str = Erreur_str.replace('  ',',')
Erreur_list = [round(float(num),8) for num in Erreur_str.replace(' ','').split(',')]
Moy = sum(Erreur_list)/len(Erreur_list)
with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\Historique.csv","a") as Historique:
	Ecriture= csv.writer(Historique)
	Ecriture.writerow([N,E,T,Erreur_str,Moy])

# Création des graphiques matplotlib:
with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_1d PRE ALPHA\\GRAPH.py","r") as script:
		exec(script.read())
	
Openg = graphique(titre='Open',x=range(len(Openp)),y=Openp,label='Valeur prédite')
Openg.courbe(range(len(Open)),Open,'Valeur réelle')
Highg = graphique(titre='High',x=range(len(Highp)),y=Highp,label='Valeur prédite')
Openg.courbe(x=range(len(High)),y=High,label='Valeur réelle')
Lowg = graphique(titre='Low',x=range(len(Lowp)),y=Lowp,label='Valeur prédite')
Openg.courbe(x=range(len(Low)),y=Low,label='Valeur réelle')
Closeg = graphique(titre='Close',x=range(len(Closep)),y=Closep,label='Valeur prédite')
Openg.courbe(x=range(len(Close)),y=Close,label='Valeur réelle')
Volumeg = graphique(titre='Volume',x=range(len(Volumep)),y=Volumep,label='Valeur prédite')
Openg.courbe(x=range(len(Volume)),y=Volume,label='Valeur réelle')

print('Entraînement terminé, afichage des données prédites:')
with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_1d PRE ALPHA\\GUI.py","r") as script:
		exec(script.read())
tk.mainloop()