import matplotlib.pyplot as plt
class graphique():
	def __init__(self,titre='Titre',x=False,y=False,label='Label'):
		self.titre = titre
		self.fenetre = plt.figure(figsize=(6, 4), dpi=100)
		if x and y != False:
			plt.plot(x,y,label=label)
		plt.title(self.titre)
		plt.legend()
	def courbe(self,x,y,label='Label'):
		plt.plot(x,y,label=label)
		plt.legend()
	def refresh(self):
		plt.clear()
		plt.draw()
	def show(self):
		plt.title(self.titre)
		plt.legend()
		plt.show()
		
x = [24,10,60,40,60,80,90,10,20,30,60]
y = [6,8,100,10,56,8,164,1030,60,80,10]
