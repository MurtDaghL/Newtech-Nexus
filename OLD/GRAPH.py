import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.axis as ax
style.use('fivethirtyeight')
# Classe graphique à 2 courbes max (sans bug):
class graphique():
	def __init__(self,titre='Titre',x='lel',y='lel',legende='légende'):
		self.titre = titre
		self.x1 = x
		self.y1 = y
		self.fenetre = plt.figure(figsize=(6, 4), dpi=100,)
		self.axes = self.fenetre.add_subplot(1,1,1)
		self.legende = legende
		if x and y != 'lel':
			self.axes.plot(x,y,label=legende)
		plt.title(self.titre)
		plt.legend()
	def courbe(self,x,y,legende='légende'):
		self.axes.plot(x,y,label=legende)
		self.axes.legend()
		self.x2 = x
		self.y2 = y
		self.legende2 = legende
	def show(self):
		plt.title(self.titre)
		plt.legend()
		plt.show()
	def refresh(self,courbe,x,y):
		if courbe == 0:
			del self.axes.lines[0]
			self.axes.plot(x,y,label=self.legende,color='b')
		elif courbe == 1:
			del self.axes.lines[1]
			self.axes.plot(x,y,label=self.legende2,color='r')
		plt.title(self.titre)
		# plt.legend()
	def anim(self,i):
		anim = animation.FuncAnimation(self.fenetre,self.refresh,interval=i,blit=True)
		return anim