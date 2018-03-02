with open("D:\\Domanis\\PYTHON\\Datas\\ANN.txt","r") as ANN3:
	exec(ANN3.read())

import matplotlib
import tkinter as tk
matplotlib.use("TkAgg")

import csv, matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


# Définition fonction de normalisation:
def norm(data,min,max):
	data = float(data)
	min = float(min)
	max = float(max)
	return (data-min)/(max-min)

def denorm(data,min,max):
	data = float(data)
	min = float(min)
	max = float(max)
	return data*(max-min)+min


# Extraction des données:
Datas_Dict = []
with open('D:\\Domanis\\PYTHON\\Datas\\aapl.csv', 'r') as aapl:
	Texte= csv.DictReader(aapl)
	for ligne in Texte:
		Datas_Dict.append(ligne)

# Séparation des données
Open = []
High = []
Low = []
Close = []
Volume = []
for ligne in Datas_Dict:
	Open.append(float(ligne['Open']))
	High.append(float(ligne['High']))
	Low.append(float(ligne['Low']))
	Close.append(float(ligne['Close']))
	Volume.append(float(ligne['Volume']))

# Définition des données dans une matrice et normalisation:
Datas = []
Datas_Norm = []

	# Données non normalisées:
for i in range(len(Datas_Dict)):
	Datas.append([Open[i],High[i],Low[i],Close[i],Volume[i]])
	# Données normalisées:
for ligne in range(len(Datas_Dict)):
	LigneMat = []
	LigneMat.append(norm(Open[ligne],min(Open),max(Open)))
	LigneMat.append(norm(High[ligne],min(High),max(High)))
	LigneMat.append(norm(Low[ligne],min(Low),max(Low)))
	LigneMat.append(norm(Close[ligne],min(Close),max(Close)))
	LigneMat.append(norm(Volume[ligne],min(Volume),max(Volume)))
	Datas_Norm.append(LigneMat)


# Suppressions de données pour l'entrainement:
Attendu = Datas_Norm
for i in range(20):
	del Attendu[0]
Input = Attendu
del Input[0]


# Conversion en arrays:
Attendu = np.array(Attendu)
Input = np.array(Input)


# Extraction liste Historique:
Perf_Dict = []
with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\Historique.csv","r") as Historique:
	Reader = csv.DictReader(Historique)
	for ligne in Reader:
		Perf_Dict.append(ligne)

N = []
E = []
T = []
Erreur = []
Err_moy = []
for ligne in Perf_Dict:
	N.append(int(ligne['Neurones']))
	E.append(int(ligne['Essais']))
	T.append(float(ligne['Taux']))
	Err_moy.append(float(ligne['Moyenne']))


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
PredictApple.apprentissage(E,T,Input,Attendu)

print('\n \n \n \n \n')

# Test de prédiction:
z = list(PredictApple.propagation(Input))

for i in range(21):
	z.insert(0,PredictApple.propagation(z[0]))

# Inversion des matrices:
z= z[::-1]
Datas = Datas[::-1]

Open = []
High = []
Low = []
Close = []
Volume = []

for i in range(len(Datas)):
	Open.append(float(Datas[i][0]))
	High.append(float(Datas[i][1]))
	Low.append(float(Datas[i][2]))
	Close.append(float(Datas[i][3]))
	Volume.append(float(Datas[i][4]))



# Dénormanisation:
Prediction = []
for i in range(len(z)):
	pa = denorm(z[i][0],min(Open),max(Open))
	pb = denorm(z[i][1],min(High),max(High))
	pc = denorm(z[i][2],min(Low),max(Low))
	pd = denorm(z[i][3],min(Close),max(Close))
	pe = denorm(z[i][4],min(Volume),max(Volume))
	PredictionLigne = [pa,pb,pc,pd,pe]
	Prediction.append(PredictionLigne)

# Séparation des données
Openp = []
Highp = []
Lowp = []
Closep = []
Volumep = []
for i in range(len(Prediction)):
	Openp.append(float(Prediction[i][0]))
	Highp.append(float(Prediction[i][1]))
	Lowp.append(float(Prediction[i][2]))
	Closep.append(float(Prediction[i][3]))
	Volumep.append(float(Prediction[i][4]))

print('Enregistrement de la performance du réseau')
Erreur = str(PredictApple.quadratique(Input,Attendu))
Erreur_str = Erreur.replace('[','')
Erreur_str = Erreur_str.replace(']','')
Erreur_list = [round(float(num),8) for num in Erreur_str.replace('  ',',').split(',')]
Moy = sum(Erreur_list)/len(Erreur_list)

with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\Historique.csv","a") as Historique:
	Ecriture= csv.writer(Historique)
	Ecriture.writerow([N,E,T,Erreur_str,Moy])







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



# Création de la fenêtre tkinter:
fenetre = tk.Tk()
fenetre.title("DONNEES DE PREDICTION")
fenetre.configure(background='white')

	# Définition éléments:


		# Graphiques:
Frame_graph =tk.Frame(fenetre,)
canv_open = FigureCanvasTkAgg(Openg,master=Frame_graph)
canv_close = FigureCanvasTkAgg(Closeg,master=Frame_graph)
canv_high = FigureCanvasTkAgg(Highg,master=Frame_graph)
canv_low = FigureCanvasTkAgg(Lowg,master=Frame_graph)
canv_volume = FigureCanvasTkAgg(Volumeg,master=Frame_graph)

		# Ecran:
Ecran = tk.LabelFrame(Frame_graph,width=580,height=380, bg ='green',bd=10,relief='sunken',text='Terminal')
Ecran.propagate(0)
Texte_screen = tk.Text(Ecran,bg='green')

		# Entrée utilisateur:
Frame_input = tk.Frame(fenetre,borderwidth=5,relief='sunken')
I1 = tk.StringVar()
Neurones = tk.Entry(Frame_input, textvariable = N,justify='center',bg='yellow')
I2 = tk.StringVar()
Essais = tk.Entry(Frame_input, textvariable = E,justify='center',bg='yellow')
I3 = tk.StringVar()
Taux = tk.Entry(Frame_input, textvariable = T,justify='center',bg='yellow')
T1 = tk.Label(Frame_input, text="Neurones de la couche intermédiaire:")
T2 = tk.Label(Frame_input, text="Nombre d'essais:")
T3 = tk.Label(Frame_input, text="Taux d'apprentissage:")




Openg.canvas.draw()
Highg.canvas.draw()
Lowg.canvas.draw()
Closeg.canvas.draw()
Volumeg.canvas.draw()


def _quit():
	fenetre.quit()
	fenetre.destroy()
def _valider():
	N = I1.get()
	E = I2.get()
	T = I3.get()
	Texte_screen.append([N,E,T])
quitter = tk.Button(Frame_input, text = "Quitter", command = _quit, width=30)
valider = tk.Button(Frame_input, text = "Valider", command = _valider, width=30)


	# Affichage éléments:


Frame_input.pack()
Neurones.grid(row=0,column=1)
Essais.grid(row=1,column=1)
Taux.grid(row=2,column=1)
T1.grid(row=0,column=0)
T2.grid(row=1,column=0)
T3.grid(row=2,column=0)
quitter.grid(row=3,column=0)
valider.grid(row=3,column=1)

Frame_graph.pack()
canv_open._tkcanvas.grid(row=0,column=0)
canv_close._tkcanvas.grid(row=0,column=1)
canv_high._tkcanvas.grid(row=1,column=0)
canv_low._tkcanvas.grid(row=1,column=1)
canv_volume._tkcanvas.grid(row=1,column=2)

Ecran.grid(row=0,column=2)
Texte_screen.pack()





print('Entraînement terminé, afichage des données prédites:')
tk.mainloop()
