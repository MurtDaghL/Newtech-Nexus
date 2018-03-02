# Création de la fenêtre tkinter:
fenetre = tk.Tk()
fenetre.title("Newtech Nexus v0.0.0_2c PRE ALPHA")
	# Définition éléments:
Frame_main =tk.Frame(fenetre)
		# Graphiques:
canv_open = FigureCanvasTkAgg(Openg.fenetre,master=Frame_main)._tkcanvas.grid(row=1,column=0)
canv_close = FigureCanvasTkAgg(Closeg.fenetre,master=Frame_main)._tkcanvas.grid(row=1,column=1)
canv_high = FigureCanvasTkAgg(Highg.fenetre,master=Frame_main)._tkcanvas.grid(row=2,column=0)
canv_low = FigureCanvasTkAgg(Lowg.fenetre,master=Frame_main)._tkcanvas.grid(row=2,column=1)
canv_volume = FigureCanvasTkAgg(Volumeg.fenetre,master=Frame_main)._tkcanvas.grid(row=2,column=2)
		# Ecran:
Ecran = tk.LabelFrame(Frame_main,width=580,height=380, bg ='green',bd=10,relief='sunken',text='Terminal',)
Ecran.propagate(0)
Texte_screen = tk.Text(Ecran,bg='green',state='disabled')
def afficher(Texte):
	Texte_screen['state'] = 'normal'
	Texte_screen.insert('end',str(Texte))
	Texte_screen.insert('end','\n')
	Texte_screen['state'] = 'disabled'
	Texte_screen.see("end")
Ecran.grid(row=1,column=2)
		# Entrée utilisateur:
def _entry(entry):
	data = entry.get()
	return data
def _valider():
	if Neurones.get() and Essais.get() and Taux.get() != None:
		N = int(Neurones.get())
		E = int(Essais.get())
		T = float(Taux.get())
		A = anim_var.get()
		if A:
			I = int(intervalle.get())
		Neurones['state'] = 'disabled'
		Essais['state'] = 'disabled'
		Taux['state'] = 'disabled'
		valider['state'] = 'disabled'
		animation['state'] = 'disabled'
		intervalle['state'] = 'disabled'
		with open("D:\\Domanis\\PYTHON\\NEWTECH_NEXUS\\0.0.0_2c PRE ALPHA\\RESEAU.py","r") as script:
			exec(script.read())
def _quit():
	fenetre.quit()
	fenetre.destroy()
def _check():
	if anim_var.get():
		intervalle['state'] = 'disabled'
		anim_var.set(False)
	else:
		intervalle['state'] = 'normal'
		anim_var.set(True)
Frame_input = tk.Frame(Frame_main,borderwidth=5,relief='sunken',width=60)
Neurones = tk.Entry(Frame_input, textvariable = 'Neurones',justify='center')
Essais = tk.Entry(Frame_input, textvariable = 'Essais',justify='center')
Taux = tk.Entry(Frame_input, textvariable = 'Taux',justify='center')
T1 = tk.Label(Frame_input, text="Neurones de la couche intermédiaire:",).grid(row=0,column=0)
T2 = tk.Label(Frame_input, text="Nombre d'essais:").grid(row=1,column=0)
T3 = tk.Label(Frame_input, text="Taux d'apprentissage:",).grid(row=2,column=0)
valider = tk.Button(Frame_input, text = "Valider", command = _valider, width=15)
quitter = tk.Button(Frame_input, text = "Quitter", command = _quit, width=30).grid(row=3,column=0)
Frame_anim = tk.Frame(Frame_main,borderwidth=5,relief='sunken',width=20)
anim_var = tk.BooleanVar()
animation = tk.Checkbutton(Frame_anim,text='Animation?',variable=False,command=_check)
T4 = tk.Label(Frame_anim, text="Intervalle de rafraichissement:").pack()
intervalle = tk.Entry(Frame_anim, textvariable = 1000,justify='center',state='disabled')

	# Affichage éléments:
Frame_anim.grid(row=0,column=1)
animation.pack()
intervalle.pack()
Frame_input.grid(row=0, column=2)
Frame_main.pack()
Neurones.grid(row=0,column=1)
Essais.grid(row=1,column=1)
Taux.grid(row=2,column=1)
valider.grid(row=3,column=1)
Texte_screen.pack()