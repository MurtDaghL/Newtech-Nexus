

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

# Définition fonction de gestions des données:
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






# Définition de la classe réseau neuronal à 3 couches:
import numpy as np
class ExtremeANN(object):
	def __init__(self,TailleInputLayer,TailleHiddenLayer,TailleOutputLayer):
		# Définition des hyper-paramètres
		self.TailleInputLayer = TailleInputLayer
		self.TailleOutputLayer = TailleOutputLayer
		self.TailleHiddenLayer = TailleHiddenLayer
		# Définition des synapses
		self.w1 = np.random.randn(self.TailleInputLayer,self.TailleHiddenLayer)
		self.w2 = np.random.randn(self.TailleHiddenLayer, self.TailleOutputLayer)
		
		
	def sigmoide(self,x,deriv=False):
		# Définition fonction d'activation
		if deriv == True:
			return np.exp(-x)/((1+np.exp(-x))**2)
		return 1/(1+np.exp(-x))
	
	
	# Version sans enregistrement:
	def propagation(self, X):
		# Définition de la méthode de propagation:
		self.z1 = np.dot(X, self.w1)
		self.X1 = self.sigmoide(self.z1)
		self.z2 = np.dot(self.X1, self.w2)
		self.X2 = self.sigmoide(self.z2)
		return self.X2
		
	def quadratique(self, Input , Attendu, deriv=False):
		# Définition fonction de coût (taux d'erreur)
		self.Sortie = self.propagation(Input)
		if deriv == True:
			delta3 = np.multiply(-(Attendu-self.Sortie), self.sigmoide(self.z2, deriv=True))
			dErreurdW2 = np.dot(self.X1.T, delta3)
        
			delta2 = np.dot(delta3, self.w2.T)*self.sigmoide(self.z1, deriv=True)
			dErreurdW1 = np.dot(Input.T, delta2)  
        
			return dErreurdW1, dErreurdW2
			
		Erreur = 0.5*sum((Attendu-self.Sortie)**2)
		return Erreur
	
	def apprentissage(self,Essais,Apprentissage,Input,Attendu,):
		for i in range(Essais):
			Erreur = self.quadratique(Input,Attendu)
			dErreurdw1,dErreurdw2 = self.quadratique(Input,Attendu,deriv=True)
			print(i+1 , ':' , Erreur)
			self.w1 = self.w1 - Apprentissage*dErreurdw1
			self.w2 = self.w2 - Apprentissage*dErreurdw2
			
	# Version avec enregistrement (non optimisé!!):
	def propagation_e(self, X,e):
		# Définition de la méthode de propagation:
		self.z1 = np.dot(X, self.w1)
		self.X1 = self.sigmoide(self.z1)
		self.z2 = np.dot(self.X1, self.w2)
		self.X2 = self.sigmoide(self.z2)
		with open(e,"w") as e:
			Ecriture= csv.writer(e)
			for ligne in range(len(self.X2)):
				Ecriture.writerow(self.X2[ligne])
		return self.X2
		
	def quadratique_e(self, Input , Attendu,e, deriv=False):
		# Définition fonction de coût (taux d'erreur)
		self.Sortie = self.propagation_e(Input,e)
		if deriv == True:
			
			delta3 = np.multiply(-(Attendu-self.Sortie), self.sigmoide(self.z2, deriv=True))
			dErreurdW2 = np.dot(self.X1.T, delta3)
        
			delta2 = np.dot(delta3, self.w2.T)*self.sigmoide(self.z1, deriv=True)
			dErreurdW1 = np.dot(Input.T, delta2)  
        
			return dErreurdW1, dErreurdW2
			
		Erreur = 0.5*sum((Attendu-self.Sortie)**2)
		return Erreur
	
	def apprentissage_e(self,Essais,Apprentissage,Input,Attendu,e):
		for i in range(Essais):
			Erreur = self.quadratique_e(Input,Attendu,e)
			dErreurdw1,dErreurdw2 = self.quadratique(Input,Attendu,deriv=True)
			print(i+1 , ':' , Erreur)
			self.w1 = self.w1 - Apprentissage*dErreurdw1
			self.w2 = self.w2 - Apprentissage*dErreurdw2