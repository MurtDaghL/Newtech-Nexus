with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_1c PRE ALPHA\\ANN.py","r") as script:
		exec(script.read())
import matplotlib, csv
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt, tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Extraction et séparation des données:
Datas_Dict = extract_csv('D:\\Domanis\\PYTHON\\Datas\\aapl.csv')
Datas_Dict = Datas_Dict[::-1]
Open = separate_dict(Datas_Dict,'Open')
High = separate_dict(Datas_Dict,'High')
Low = separate_dict(Datas_Dict,'Low')
Close = separate_dict(Datas_Dict,'Close')
Volume = separate_dict(Datas_Dict,'Volume')

# Définition des données dans une matrice et normalisation:
Datas = []
Datas_Norm = []
for i in range(len(Datas_Dict)):
	Datas.append([Open[i],High[i],Low[i],Close[i],Volume[i]])
	Datas_Norm.append([norm(Open[i],min(Open),max(Open)),norm(High[i],min(High),max(High)),norm(Low[i],min(Low),max(Low)),norm(Close[i],min(Close),max(Close)),norm(Volume[i],min(Volume),max(Volume))])

# Suppressions de données pour l'entrainement:
Attendu = Datas_Norm
for i in range(20):
	del Attendu[len(Attendu)-1]
Input = Attendu
del Input[len(Input)-1]

Attendu = np.array(Attendu)
Input = np.array(Input)

# Extraction liste Historique:
Perf_Dict = extract_csv("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\Historique.csv")

N = separate_dict(Perf_Dict, 'Neurones')
E = separate_dict(Perf_Dict, 'Essais')
T = separate_dict(Perf_Dict, 'Taux')
Err_moy = separate_dict(Perf_Dict, 'Moyenne')
	
# Affiche performance optimale:
index = Err_moy.index(min(Err_moy))
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
# PredictApple.apprentissage_e(E,T,Input,Attendu,'D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_1c PRE ALPHA\\propagation.csv')
PredictApple.apprentissage(E,T,Input,Attendu)
print('\n \n \n \n \n')
# Prédiction des données supprimées:
# PredictApple.propagation_e(Input,'D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_1c PRE ALPHA\\propagation.csv')
PredictApple.propagation(Input)
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
Openg = plt.figure(figsize=(6, 4), dpi=100)
plt.plot(range(len(Openp)),Openp, label='Valeur prédite')
plt.plot(range(len(Open)),Open, label ='Valeur réelle')
plt.title('Open')
plt.legend()

Highg = plt.figure(figsize=(6, 4), dpi=100)
plt.plot(range(len(Highp)),Highp, label='Valeur prédite')
plt.plot(range(len(High)),High, label ='Valeur réelle')
plt.title('High')
plt.legend()

Lowg = plt.figure(figsize=(6, 4), dpi=100)
plt.plot(range(len(Lowp)),Lowp, label='Valeur prédite')
plt.plot(range(len(Low)),Low, label ='Valeur réelle')
plt.title('Low')
plt.legend()

Closeg = plt.figure(figsize=(6, 4), dpi=100)
plt.plot(range(len(Closep)),Closep, label='Valeur prédite')
plt.plot(range(len(Close)),Close, label ='Valeur réelle')
plt.title('Close')
plt.legend()

Volumeg = plt.figure(figsize=(6, 4), dpi=100)
plt.plot(range(len(Volumep)),Volumep, label='Valeur prédite')
plt.plot(range(len(Volume)),Volume, label ='Valeur réelle')
plt.title('Volume')
plt.legend()

	# Appel de l'interface:
with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_1c PRE ALPHA\\GUI.py","r") as script:
	exec(script.read())
print('Entraînement terminé, afichage des données prédites:')
tk.mainloop()