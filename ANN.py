import numpy as np
from numpy.linalg import norm

# Définition fonction de normalisation:
def MMnorm(data,min,max): # MinMax normalisation:
	data = float(data)
	min = float(min)
	max = float(max)
	return (data-min)/(max-min)

def MMdenorm(data,min,max):
	data = float(data)
	min = float(min)
	max = float(max)
	return data*(max-min)+min


class Neural_Network(object):
#Définition des fonctions du réseau
		self.Agregation = np.dot #Produit matriciel
		self.Activation = self.sigmoide #Sigmoïde
		self.Erreur = 'Quadratique'
		self.BackProp = 'Descente gradiente'
	#Fonctions d'activation (Avec P un paramètre de la fonction)
	def sigmoide(self,x,deriv=False,P=1):
		if deriv == True:
			return P*np.exp(-P*x)/((1+np.exp(-P*x))**2)
		return 1/(1+np.exp(-P*x))

	def tanh(self,x,deriv=False):
		if deriv == True:
			return 1 - (np.tanh(x))**2
		return np.tanh(x)
	# Fonctions d'agrégation:
	def hadamard(self,x,y):
		return x*y

class ExtremeANN(Neural_Network): # Définition de la classe réseau neuronal à 3 couches:
	def __init__(self,TailleInputLayer,TailleHiddenLayer,TailleOutputLayer):
		Neural_Network.__init__(self)
		# Définition des hyper-paramètres
		self.TailleInputLayer = TailleInputLayer
		self.TailleOutputLayer = TailleOutputLayer
		self.TailleHiddenLayer = TailleHiddenLayer
		# Définition des synapses
		self.w1 = np.random.randn(self.TailleInputLayer,self.TailleHiddenLayer)
		self.w2 = np.random.randn(self.TailleHiddenLayer, self.TailleOutputLayer)
		# Définition des gradients (utile pour le gradient check)
		self.dErreurdW2 = False
		self.dErreurdW1 = False

	def propagation(self, X): # Définition de la méthode de propagation:
		self.input = X
		self.z1 = self.Agregation(X, self.w1)
		self.X1 = self.Activation(self.z1)
		self.z2 = self.Agregation(self.X1, self.w2)
		self.X2 = self.Activation(self.z2)
		return self.X2

	def quadratique(self, Input , Attendu, deriv=False): # Définition fonction de coût (taux d'erreur):
		self.attendu = Attendu
		self.Sortie = self.propagation(Input)
		if deriv == True:
			delta3 = np.multiply(-(Attendu-self.Sortie), self.Activation(self.z2, deriv=True))
			self.dErreurdW2 = np.dot(self.X1.T, delta3)

			delta2 = np.dot(delta3, self.w2.T)*self.Activation(self.z1, deriv=True)
			self.dErreurdW1 = np.dot(np.array(Input).T, delta2)

			return self.dErreurdW1, self.dErreurdW2

		Erreur = 0.5*sum((Attendu-self.Sortie)**2)
		return Erreur

	def apprentissage(self,Essais,Apprentissage,Input,Attendu,):
		for i in range(Essais):
			Erreur = self.quadratique(Input,Attendu)
			dErreurdw1,dErreurdw2 = self.quadratique(Input,Attendu,deriv=True)
			print(i+1 , ':' , Erreur)
			self.w1 = self.w1 - Apprentissage*dErreurdw1
			self.w2 = self.w2 - Apprentissage*dErreurdw2

	def get_synapse(self): # Permet de récupérer W1 et W2 dans un vecteur
		return np.concatenate(self.w1.ravel(),self.w2.ravel())

	def set_synapse(self,vecteur): # Permet de définir W1 et W2 avec un vecteur
		debut = 0
		w1_fin = self.TailleHiddenLayer*self.TailleInputLayer
		self.w1 = np.reshape(vecteur[debut:w1_fin],(self.TailleInputLayer,self.TailleHiddenLayer))
		w2_fin = w1_fin + self.TailleHiddenLayer*self.TailleOutputLayer
		self.w2 = np.reshape(vecteur[debut:w2_fin],(self.TailleHiddenLayer,self.TailleOutputLayer))

	def gradient(self): # Permet de récupérer dErreurdW1 et dErreurdW2 dans un vecteur
		return np.concatenate(self.dErreurW1.ravel(),self.dErreurW2.ravel())

	def calcul_gradient(self,x,y): # Permet de récupérer dErreurdW1 et dErreurdW2 dans un vecteur (calcul)
		dErreurW1, dErreurW2 = self.quadratique(x,y,deriv=True)
		return np.concatenate(dErreurW1.ravel(),dErreurW2.ravel())

	def calcul_numgradient(self,x,y): # Calcule le gradient numérique (approximation du gradient)
		param_init = self.get_synapse()
		numgrad = np.zeroes(param_init.shape)
		perturb = np.zeroes(param_init.shape)
		E = 10**-4
		for i in range(len(param_init)):
			# Perturbation:
			perturb[i] = E
			self.set_synapse(param_init + perturb)
			erreur2 = self.quadratique(x,y)
			self.set_synapse(param_init - perturb)
			erreur1 = self.quadratique(x,y)
			# Calcul gradient numérique:
			numgrad[i] = (erreur2-erreur1)/(2*E)
			perturb[i] = 0
		return numgrad

	def gradient_check(self): # Calcul de la différence entre le gradient numérique et le gradient
		if self.dErreurdW1 and self.dErreurdW2 != False:
			grad = self.gradient()
			numgrad = self.calcul_numgradient()
		else:
			grad = self.calcul_gradient()
			numgrad = self.calcul_numgradient()
		return norm(grad-numgrad)/norm(grad+numgrad)
