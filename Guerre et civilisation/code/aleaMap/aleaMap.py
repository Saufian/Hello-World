# -*- coding: utf-8 -*-
import sys, pygame
from random import randint
pygame.init()

size = width, height = 641, 641
tailleCase=5
screen = pygame.display.set_mode(size)

#color=[(124, 16, 240), (122, 24, 232), (120, 32, 224), (118, 40, 216), (116, 48, 208), (114, 56, 200), (112, 64, 192), (110, 72, 184), (108, 80, 176), (106, 88, 168), (104, 96, 160), (102, 104, 152), (100, 112, 144), (98, 120, 136), (96, 128, 128), (94, 136, 120), (92, 144, 112), (90, 152, 104), (88, 160, 96), (86, 168, 88), (84, 176, 80), (82, 184, 72), (80, 192, 64), (78, 200, 56), (76, 208, 48), (74, 216, 40), (72, 224, 32), (70, 232, 24), (68, 240, 16), (66, 248, 8), (8, 248, 32), (16, 240, 32), (24, 232, 32), (32, 224, 32), (40, 216, 32), (48, 208, 32), (56, 200, 32), (64, 192, 32), (72, 184, 32), (80, 176, 32), (88, 168, 32), (96, 160, 32), (104, 152, 32), (112, 144, 32), (120, 136, 32), (128, 128, 32), (136, 120, 32), (144, 112, 32), (152, 104, 32), (160, 96, 32), (168, 88, 32), (176, 80, 32), (184, 72, 32), (192, 64, 32), (200, 56, 32), (208, 48, 32), (216, 40, 32), (224, 32, 32), (232, 24, 32), (240, 16, 32), (248, 8, 32)]
color=[(124, 16, 240), (122, 24, 232), (120, 32, 224), (118, 40, 216), (116, 48, 208), (114, 56, 200), (112, 64, 192), (110, 72, 184), (108, 80, 176), (106, 88, 168), (104, 96, 160), (102, 104, 152), (100, 112, 144), (98, 120, 136), (96, 128, 128), (94, 136, 120), (92, 144, 112), (90, 152, 104), (88, 160, 96), (86, 168, 88), (84, 176, 80), (82, 184, 72), (80, 192, 64), (78, 200, 56), (76, 208, 48), (74, 216, 40), (72, 224, 32), (70, 232, 24), (68, 240, 16), (66, 248, 8), (8, 248, 32), (16, 240, 32), (24, 232, 32), (32, 224, 32), (40, 216, 32), (48, 208, 32), (56, 200, 32), (64, 192, 32), (72, 184, 32), (80, 176, 32), (88, 168, 32), (96, 160, 32), (104, 152, 32), (112, 144, 32), (120, 136, 32), (128, 128, 32), (136, 120, 32), (144, 112, 32), (152, 104, 32), (160, 96, 32), (168, 88, 32), (176, 80, 32), (184, 72, 32), (192, 64, 32), (200, 56, 32), (208, 48, 32), (216, 40, 32), (224, 32, 32), (232, 24, 32), (240, 16, 32), (248, 8, 32)]


class unit:
	def __init__(self,dataNiv=0,pos=(0,0)):#avec pos un tuple de la forme (posX,posY)
		self.niveau=dataNiv#niveau (d'entre -30 et 30 inclu)
		self.posX=pos[0]
		self.posY=pos[1]
	
	def setNiveau(self, niv):
		self.niveau=niv#niveau (entre -30 et 30 inclu)
	
	def setPos(self,x,y):
		self.posX=x
		self.posY=y
	
	def getPos(self):
		return(self.posX,self.posY)
	
	def getColor(self):
		return(color[self.niveau+30])


def affiche(terrain):
	for x in range(width//tailleCase):
		for y in range(height//tailleCase):
			pygame.draw.rect(screen, terrain[x][y].getColor(), (x*tailleCase,y*tailleCase,(x+1)*tailleCase,(y+1)*tailleCase))#on fait des carres
	pygame.display.flip()
	#while 1:
	#	for event in pygame.event.get():
	#		if event.type == pygame.QUIT: sys.exit()


def pic(terrain, nb, mini, maxi, difA0, eloignement, listePic=[]):#eloignement correspond au nombre de cases entre le point et les autres (fonctionne sous forme de carrés)
	if mini==0:#on change la valeur de base: on evite les 0 lors des divisions
		mini=1
	if maxi==0:
		maxi=-1
		
	if abs(mini)<difA0:#on limite la taille des pics : on ne veux pas qu'ils soient plus petit que difA0
		mini=difA0*(mini//abs(mini))#si le minimum de taille de pic est trop faible, on le met a la limite de difA0, en respectant son signe
	if abs(maxi)<difA0:#meme chose avec le maximum
		maxi=difA0*(maxi//abs(maxi))
	xMax=len(terrain)-1#on evite les depassements de variables
	yMax=len(terrain[0])-1
	compt=0#compteur de pics realise dans cet appel
	limite=nb*10#nombre maximum d'iteration, pour eviter la boucle infini
	comptCritique=0#compteur associé
	while compt < nb and comptCritique<limite:#on s'arrete quand tout est créé, ou si on atteint le nombre max d'iteration
		comptCritique+=1
		x=randint(0,xMax)#position aleatoire
		y=randint(0,yMax)
		vide=True#test sur la presence ou non de pics sur et autour de la position de 
		for p in listePic:#on test sur chaque pic deja existant
			if p.getPos()[0]>=x-eloignement and p.getPos()[0]<=x+eloignement and p.getPos()[1]>=y-eloignement and p.getPos()[1]<=y+eloignement and vide:#si une position est deja prise
				vide=False
		if vide:#si la place est libre, on crée un nouveau pic
			nouvNiveau=0
			comptCrit=0
			while nouvNiveau==0:
				nouvNiveau=randint(mini-(difA0*(mini//abs(mini))), maxi-(difA0*(maxi//abs(maxi))))#on met un aleatoire qui va donner une valeur dans l'interval entre l'ecart et la limite(l'interval est plus petit, mais les signes sont respecté)
				comptCrit+=1
				if comptCrit==50:#50 tentatives et que des 0 : on sort en donnant un résultat neutre
					nouvNiveau=1
			nouvNiveau=nouvNiveau+difA0*(nouvNiveau//abs(nouvNiveau))#on rajoute la diference à 0, en faisant attention au signe
			terrain[x][y].setNiveau(nouvNiveau)
			listePic.append(terrain[x][y])
			compt+=1#un pic de plus, on ingremente le curseur
	if comptCritique==limite:
		print("maximum d'iteration atteint")#averti du fait que l'on ai depassé le nombre limite
	return(listePic)


def descente(terrain,listePic,pente):#avec la pente en pourcentage
	listeFait=[]#contient les coordonnées (x,y) de la position des elements de terrain deja calculé
	if pente>100:
		pente=100
	compt=0
	listeTrv=[i.getPos() for i in listePic]#creation d'une liste contenant les positions des cases à travailler
	while len(listeTrv)!=0:#s'arrete quand la liste est vide
		for x in range(listeTrv[-1][0]-1,listeTrv[-1][0]+2):#on prend les cases proches
			for y in range(listeTrv[-1][1]-1,listeTrv[-1][1]+2):
				if x>=0 and x<len(terrain) and y>=0 and y<len(terrain[0]):#on evite de sortir du terrain
					if not((x,y) in listeFait):#s'il n'a pas été déjà fait
						tauxDescente=terrain[listeTrv[-1][0]][listeTrv[-1][1]].niveau//(101-pente)
						if tauxDescente==0:
							tauxDescente=1
						if terrain[listeTrv[-1][0]][listeTrv[-1][1]].niveau<0:#cas où le pic est plus bas
							if terrain[listeTrv[-1][0]][listeTrv[-1][1]].niveau<terrain[x][y].niveau:#si le terrain proche doit etre abaissé (on ne fait pas monter des cases plus basse)
								terrain[x][y].setNiveau(terrain[listeTrv[-1][0]][listeTrv[-1][1]].niveau+randint(1,(-1*tauxDescente)))#on fait monter les zones proches
								if not((x,y) in listeTrv):# on pensera a regarder ce terrain, on evite les repetitions et ce qui est deja fait
									listeTrv.append(terrain[x][y].getPos())
						elif terrain[listeTrv[-1][0]][listeTrv[-1][1]].niveau>0:#cas dans lequel le terrain est plus haut que le sol
							if terrain[listeTrv[-1][0]][listeTrv[-1][1]].niveau>terrain[x][y].niveau:#si le terrain proche doit etre monté (on ne fait pas descendre des cases plus haute)
								terrain[x][y].setNiveau(terrain[listeTrv[-1][0]][listeTrv[-1][1]].niveau-randint(1,(tauxDescente)))#on fait descendre les zones proches
								if not((x,y) in listeTrv):# on pensera a regarder ce terrain, on evite les repetitions et ce qui est deja fait
									listeTrv.append(terrain[x][y].getPos())
		listeFait.append(listeTrv[-1])
		del listeTrv[-1]
		#print("listeTrv = ",len(listeTrv),"  listeFait = ",len(listeFait))
		#if len(listeFait)>1+compt:
		#	compt=len(listeFait)
		#	affiche(terrain)
	return(listeFait)


#terrain=[[unit(int((i+j)*(float(len(color))/float((width//tailleCase)+(height//tailleCase))))-30) for j in range(height//tailleCase)]for i in range (width//tailleCase)]

terrain=[[unit(0,(i,j)) for j in range(height//tailleCase)]for i in range (width//tailleCase)]

listePic=pic(terrain, 20,-30,30,15,9)

test=descente(terrain,listePic,0)

affiche(terrain)



