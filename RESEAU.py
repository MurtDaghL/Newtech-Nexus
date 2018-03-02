plt.close('all')
# Apprentissage:
Apple = ExtremeANN(5,N,5)
for i in range(E):
	Erreur = Apple.quadratique(Input,Attendu)
	dErreurdw1,dErreurdw2 = Apple.quadratique(Input,Attendu,deriv=True)
	afficher('{Essai}:{Erreur}'.format(Essai=i+1,Erreur=Erreur))
	Texte_screen.see("end")
	Apple.w1 = Apple.w1 - T*dErreurdw1
	Apple.w2 = Apple.w2 - T*dErreurdw2

		# Dénormanisation et séparation:
	if i%10 == 0:
		Openp = []
		Highp = []
		Lowp = []
		Closep = []
		Volumep = []
		for i in range(len(Apple.X2)):
			Openp.append(denorm(Apple.X2[i][0],min(Open),max(Open)))
			Highp.append(denorm(Apple.X2[i][1],min(High),max(High)))
			Lowp.append(denorm(Apple.X2[i][2],min(Low),max(Low)))
			Closep.append(denorm(Apple.X2[i][3],min(Close),max(Close)))
			Volumep.append(denorm(Apple.X2[i][4],min(Volume),max(Volume)))
		# Raffraichissement des graphs:
		Openg.refresh(1,x=range(len(Openp)),y=Openp)
		Highg.refresh(1,x=range(len(Highp)),y=Highp)
		Lowg.refresh(1,x=range(len(Lowp)),y=Lowp)
		Closeg.refresh(1,x=range(len(Closep)),y=Closep)
		Volumeg.refresh(1,x=range(len(Volumep)),y=Volumep)
		plt.pause(0.00001)
		
		# Raffraichissement des graphs dans tkinter:
		canv_open = FigureCanvasTkAgg(Openg.fenetre,master=Frame_main)._tkcanvas.grid(row=1,column=0)
		canv_close = FigureCanvasTkAgg(Closeg.fenetre,master=Frame_main)._tkcanvas.grid(row=1,column=1)
		canv_high = FigureCanvasTkAgg(Highg.fenetre,master=Frame_main)._tkcanvas.grid(row=2,column=0)
		canv_low = FigureCanvasTkAgg(Lowg.fenetre,master=Frame_main)._tkcanvas.grid(row=2,column=1)
		canv_volume = FigureCanvasTkAgg(Volumeg.fenetre,master=Frame_main)._tkcanvas.grid(row=2,column=2)
		
afficher('\n \n \n \n \n')
# Prédiction des données supprimées:
z = list(Apple.propagation(Input))
for i in range(21):
	z.insert(len(z)-1,Apple.propagation(z[len(z)-1]))

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
# Raffraichissement des graphs:
Openg.refresh(1,x=range(len(Openp)),y=Openp)
Highg.refresh(1,x=range(len(Highp)),y=Highp)
Lowg.refresh(1,x=range(len(Lowp)),y=Lowp)
Closeg.refresh(1,x=range(len(Closep)),y=Closep)
Volumeg.refresh(1,x=range(len(Volumep)),y=Volumep)	
	
afficher('Enregistrement de la performance du reseau')
Erreur = str(Apple.quadratique(Input,Attendu))
Erreur_str = Erreur.replace('[','')
Erreur_str = Erreur_str.replace(']','')
Erreur_str = Erreur_str.replace('  ',',')
Erreur_list = [round(float(num),8) for num in Erreur_str.replace(' ','').split(',')]
Moy = sum(Erreur_list)/len(Erreur_list)
with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\Historique.csv","a") as Historique:
	Ecriture= csv.writer(Historique)
	Ecriture.writerow([N,E,T,Erreur_str,Moy])
afficher('Enregistrement termine')