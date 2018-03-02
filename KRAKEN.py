with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_1b PRE ALPHA\\ANN.txt","r") as ANN:
	exec(ANN.read())

import matplotlib, csv
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt, tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


def extract_csv(chemin):
	import csv
	Datas_Dict = []
	with open(chemin, 'r') as fichier:
		Texte= csv.DictReader(fichier)
		for ligne in Texte:
			Datas_Dict.append(ligne)
	return Datas_Dict
	
def separate_dict(Dict, Data):
	Liste = []
	for ligne in Dict:
		Liste.append(float(ligne[Data]))
	return Liste
	
# Extraction des données
Datas_Dict = extract_csv('D:\\Domanis\\PYTHON\\Datas\\aapl.csv')
# Inversion des données
Datas_Dict = Datas_Dict[::-1]
# Séparation des données
Open = separate_dict(Datas_Dict,'Open')
High = separate_dict(Datas_Dict,'High')
Low = separate_dict(Datas_Dict,'Low')
Close = separate_dict(Datas_Dict,'Close')
Volume = separate_dict(Datas_Dict,'Volume')


# Définition des données dans une matrice et normalisation:
Datas = []
Datas_Norm = []
for i in range(len(Datas_Dict)):
	# Données non normalisées:
	Datas.append([Open[i],High[i],Low[i],Close[i],Volume[i]])
	# Données normalisées:
	Datas_Norm.append([norm(Open[i],min(Open),max(Open)),norm(High[i],min(High),max(High)),norm(Low[i],min(Low),max(Low)),norm(Close[i],min(Close),max(Close)),norm(Volume[i],min(Volume),max(Volume))])

	
# Suppressions de données pour l'entrainement:
Attendu = Datas_Norm
for i in range(20):
	del Attendu[len(Attendu)-1]
Input = Attendu
del Input[len(Input)-1]


# Conversion en arrays:
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
PredictApple.apprentissage(E,T,Input,Attendu)

print('\n \n \n \n \n')

z = list(PredictApple.propagation(Input))

for i in range(21):
	z.insert(len(z)-1,PredictApple.propagation(z[len(z)-1]))

# Dénormanisation:
Prediction = []
for i in range(len(z)):
	pa = denorm(z[i][0],min(Open),max(Open))
	pb = denorm(z[i][1],min(High),max(High))
	pc = denorm(z[i][2],min(Low),max(Low))
	pd = denorm(z[i][3],min(Close),max(Close))
	pe = denorm(z[i][4],min(Volume),max(Volume))
	Prediction.append([pa,pb,pc,pd,pe])
	
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



# Création de la fenêtre tkinter:
fenetre = tk.Tk()
fenetre.title("Newtech Nexus v0.0.0_1b PRE ALPHA")


	# Définition éléments:

		
		# Graphiques:
Frame_main =tk.Frame(fenetre,bg='white')
canv_open = FigureCanvasTkAgg(Openg,master=Frame_main)
canv_close = FigureCanvasTkAgg(Closeg,master=Frame_main)
canv_high = FigureCanvasTkAgg(Highg,master=Frame_main)
canv_low = FigureCanvasTkAgg(Lowg,master=Frame_main)
canv_volume = FigureCanvasTkAgg(Volumeg,master=Frame_main)
Openg.canvas.draw()
Highg.canvas.draw()
Lowg.canvas.draw()
Closeg.canvas.draw()
Volumeg.canvas.draw()

		# Ecran:
		
Ecran = tk.LabelFrame(Frame_main,width=580,height=380, bg ='green',bd=10,relief='sunken',text='Terminal',)
Ecran.propagate(0)

Texte_screen = tk.Text(Ecran,bg='green',state='disabled')
def afficher(Texte):
	Texte_screen['state'] = 'normal'
	Texte_screen.insert('end',str(Texte))
	Texte_screen.insert('end','\n')
	Texte_screen['state'] = 'disabled'
		
		# Entrée utilisateur:
Frame_input = tk.Frame(Frame_main,borderwidth=5,relief='sunken',width=60)
I1 = tk.StringVar()
Neurones = tk.Entry(Frame_input, textvariable = I1,justify='center')
I2 = tk.StringVar()
Essais = tk.Entry(Frame_input, textvariable = I2,justify='center')
I3 = tk.StringVar()
Taux = tk.Entry(Frame_input, textvariable = I3,justify='center')
T1 = tk.Label(Frame_input, text="Neurones de la couche intermédiaire:",)
T2 = tk.Label(Frame_input, text="Nombre d'essais:")
T3 = tk.Label(Frame_input, text="Taux d'apprentissage:",)
def _valider():
	N = I1.get()
	E = I2.get()
	T = I3.get()
	Neurones['bg'] = 'green'
	Essais['bg'] = 'green'	
	Taux['bg'] = 'green'
	Neurones['state'] = 'disabled'
	Essais['state'] = 'disabled'
	Taux['state'] = 'disabled'
	valider.destroy()
	afficher(N)
	afficher(E)
	afficher(T)
valider = tk.Button(Frame_input, text = "Valider", command = _valider, width=15)
def _quit():
	fenetre.quit()
	fenetre.destroy()
quitter = tk.Button(Frame_input, text = "Quitter", command = _quit, width=30)
	
	# Affichage éléments:
	
Frame_main.pack()
canv_open._tkcanvas.grid(row=1,column=0)
canv_close._tkcanvas.grid(row=1,column=1)
canv_high._tkcanvas.grid(row=2,column=0)
canv_low._tkcanvas.grid(row=2,column=1)
canv_volume._tkcanvas.grid(row=2,column=2)

Frame_input.grid(row=0, column=2)
Neurones.grid(row=0,column=1)
Essais.grid(row=1,column=1)
Taux.grid(row=2,column=1)
T1.grid(row=0,column=0)
T2.grid(row=1,column=0)
T3.grid(row=2,column=0)
quitter.grid(row=3,column=0)
valider.grid(row=3,column=1)


Ecran.grid(row=1,column=2)
Texte_screen.pack()




	
print('Entraînement terminé, afichage des données prédites:')
tk.mainloop()