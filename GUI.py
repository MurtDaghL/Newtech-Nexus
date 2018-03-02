# Création de la fenêtre tkinter:
fenetre = tk.Tk()
fenetre.title("Newtech Nexus v0.0.0_1c PRE ALPHA")
	# Définition éléments:
	
		# Graphiques:
Frame_main =tk.Frame(fenetre,bg='white')
canv_open = FigureCanvasTkAgg(Openg,master=Frame_main)._tkcanvas.grid(row=1,column=0)
Openg.canvas.draw()
canv_close = FigureCanvasTkAgg(Closeg,master=Frame_main)._tkcanvas.grid(row=1,column=1)
Closeg.canvas.draw()
canv_high = FigureCanvasTkAgg(Highg,master=Frame_main)._tkcanvas.grid(row=2,column=0)
Highg.canvas.draw()
canv_low = FigureCanvasTkAgg(Lowg,master=Frame_main)._tkcanvas.grid(row=2,column=1)
Lowg.canvas.draw()
canv_volume = FigureCanvasTkAgg(Volumeg,master=Frame_main)._tkcanvas.grid(row=2,column=2)
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
	
Ecran.grid(row=1,column=2)
		
		# Entrée utilisateur:
def _entry(entry):
	data = entry.get()
	return data
def _valider():
	afficher(Neurones.get())
	afficher(Essais.get())
	afficher(Taux.get())
	Neurones['state'] = 'disabled'
	Essais['state'] = 'disabled'
	Taux['state'] = 'disabled'
	valider.destroy()
		
def _quit():
	fenetre.quit()
	fenetre.destroy()

Frame_input = tk.Frame(Frame_main,borderwidth=5,relief='sunken',width=60)
Neurones = tk.Entry(Frame_input, textvariable = 'Neurones',justify='center')
Essais = tk.Entry(Frame_input, textvariable = 'Essais',justify='center')
Taux = tk.Entry(Frame_input, textvariable = 'Taux',justify='center')
T1 = tk.Label(Frame_input, text="Neurones de la couche intermédiaire:",).grid(row=0,column=0)
T2 = tk.Label(Frame_input, text="Nombre d'essais:").grid(row=1,column=0)
T3 = tk.Label(Frame_input, text="Taux d'apprentissage:",).grid(row=2,column=0)
valider = tk.Button(Frame_input, text = "Valider", command = _valider, width=15)
quitter = tk.Button(Frame_input, text = "Quitter", command = _quit, width=30).grid(row=3,column=0)

	# Affichage éléments:
Frame_input.grid(row=0, column=2)
Frame_main.pack()
Neurones.grid(row=0,column=1)
Essais.grid(row=1,column=1)
Taux.grid(row=2,column=1)
valider.grid(row=3,column=1)
Texte_screen.pack()