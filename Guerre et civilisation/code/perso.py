  #  -*- coding: utf-8 -*-
import copy    #  pour pouvoir travailler sur des maps avec les perso sans modifier les maps originales.
from map import *

class Perso:  # permet de creer des objets personnages(en mouvement sur la map)
	def __init__(self, ID, stat=[[],[]]):  # un identifiant, et une liste de stats (par defaut : deja faite mais vide) de la forme [[a],[x]]
		self.ID = ID
		self.stat=stat
		self.graphism="none"
		self.oldGraphism="none"  # graphisme reservé pour l'affichage sur le terminal pour le debuggage
		self.setCoord(0,0)
		self.spe=[]  # creation de caractèristiques speciales (de type booleen (ex: nage ou nage pas))
		self.travel=[["vide","lave","plaine","montagne","eau","foret","spawn","objectif"],[-1,-1,0,3,3,2,0,1]]  # difficulté a traverser une case de terrain donné
					  # (de la forme [[type terrain],[dif]] (liste non exhaustive)
	
	def setCoord(self,x,y):  # mise en place et modifications des coordonnees du personnage sur les maps
		self.x=x
		self.y=y
	
	def getCoord(self):  # retour des coordonnees du personnage
		return [self.x,self.y]
	
	def difTravel(self,typ,nb):  # calcul de la difficulté d'un voyage (type du terrain, deplacement sans la difficulté)
		if typ in self.travel[0]:  # si le terrain est repertorié
			position=self.travel[0].index(typ)  # position de la donnée relative à ce terrain dans la liste
			dif=self.travel[1][position]  # difficulté associer à ce terrain
			return(nb+dif)  # retourne l'éloignement plus la difficulté de traverser
		else:
			print("Land type unknow : "+str(typ))  # affiche un message d'erreur si le terrain est inconnu
			return (-1)  # rend le terrain impraticable
	
	def addSpe(self,special):  # permet d'ajouter une capacité speciale
		self.spe.append(special)
	
	def delSpe(self,special):  # permet de retirer une capacité speciale
		if special in self.spe:  # si la capacité speciale est presente
			del self.spe[self.spe.index(special)]  # suppression de la capacité speciale
		else:
			print("this special doesn't exist")  # sinon, affichage d'un message d'erreur
	
	def getSpe(self,special):  # retourne la possession ou non de la capacité "special"
		return(special in self.spe)
	
	def setGraphism(self,graph):  # mise en place de l'affichage du personnages (skin)
		self.graphism=graph
	
	def getGraphism(self):  # renvoi le skin du personnage
		if self.graphism != "none":
			return self.graphism
		else:
			print("no skin")
			return(self.ID)
	
	def setOldGraphism(self,graph):  # mise en place de l'affichage du personnages (skin) pour la version developpeur (une lettre, un symbole)
		self.oldGraphism=graph
	
	def getOldGraphism(self):  # renvoi le skin du personnage pour l'affichage dans le terminal (une lettre, un symbole)
		if self.oldGraphism != "none":
			return self.oldGraphism
		else:
			print("no skin")
			return(self.ID)
	
	def addStat(self,nameStat,nb):  # ajout de Statistique au personnage (nom de la nouvelle stat, valeur initial)
		if nameStat in self.stat[0]:
			self.changeStat(nameStat,nb)
			print("Stat already create")
		else:
			self.stat[0].append(nameStat)
			self.stat[1].append(nb)
	
	def changeStat(self,nameStat,nb):  # changement de valeur d'une stat deja possedé (nom de la stat, nouvelle valeur)
		if nameStat in self.stat[0]:  # test pour savoir si la statistique existe avant de la changer.
			position=self.stat[0].index(nameStat)
			self.stat[1][position]=nb
		else:
			print("no stat")  # sinon, message d'erreur
	
	def getStat(self,nameStat):  # retourne l'etat de la stat "nameStat"
		if nameStat in self.stat[0]:  # si c'est une stat qui est dans la liste
			position=self.stat[0].index(nameStat)  # trouve la position de la stat
			return self.stat[1][position]  # retourne la valeur associé
		else:
			print("no stat")  # sinon ->message d'erreur
	
	def delStat(self, nameStat):
		if nameStat in self.stat[0]:  # si c'est une stat qui est dans la liste
			position=self.stat[0].index(nameStat)  # trouve la position de la stat
			del self.stat[0][position]
			del self.stat[1][position]  # retourne la valeur associé
		else:
			print("no stat")  # sinon ->message d'erreur
	
	
	
	def printOldPerso(self,nMap):  # affichage de la carte+le perso
		work=copy.deepcopy(nMap)  # clonage des données de base de la carte
		position=self.getCoord()  # recuperation de la position des perso
		if position[0]>=0 and position[0]<len(work) and position[1]>=0 and position[1]<len(work[0]):  # securité pour eviter les dépassement hors 					tableau
			work.contenu[position[0]][position[1]]=self  # remplacement de l'objet dans le tableau(on peut y faire en meme temps pour d'autres Perso)
		testPrintMap(work)  # affichage de la map modifiée
	
	def printPerso(self,nMap,screen,):  # affichage de la carte+le perso ( sur un ecran de taille screenWidth, screenHeight, donné par screen.getSize()[0] et screen.getSize()[1])
		position=self.getCoord()  # recuperation de la position des perso
		dataMap=nMap.printMap(screen,refresh=False)
		screen.setSurface(dataMap[0])  # recuperation des graphismes de la map
		tailleX=dataMap[1]
		tailleY=dataMap[2]
		if position[0]>=0 and position[0]<len(nMap.contenu) and position[1]>=0 and position[1]<len(nMap.contenu[0]):  # securité pour eviter les dépassement hors tableau
			skin=pygame.transform.scale(self.getGraphism(),(tailleX,tailleY))
			 # work[position[0]][position[1]]=self  # remplacement du de l'objet dans le tableau (on peut y faire en meme temps pour d'autres Perso)
			pygame.display.flip()
			screen.getSurface().blit(skin,(position[0]*tailleX,position[1]*tailleY))  # remplacement de l'objet dans le tableau (on peut y faire en meme temps pour d'autres Perso)
		pygame.display.flip()
	
	def testMove(self,maps,listePerso=[]):  # affiche la map avec la valeur nescessaire au deplacement (avec la liste des position deja prise)
		if len(listePerso)==0:  # si la liste est vide
			listePerso.append(self)  # mettre le personnage "self" dedans 
		save=copy.deepcopy(maps.contenu)  # on creer une sauvegarde independante de la carte de base
		liste=[]  # creation de la liste dans laquelle on ira stocker les differentes valeurs de déplacement, triées en fonction de la difficulté
		work=cloneList(save)  # work devient une copie de save
		maxi=len(save)*len(save[0])+1  # on ajoute 1 pour étre sur que cette valeur ne sera pas dépassable
		for i in range(maxi):   # creation de la liste de coordonnees des differentes valeurs (de 0 à maxi)
			liste.append([i,[],[]])  # la liste des valeurs est de la forme:[dif,[liste des abscisses des cases ayant cette difficulté],[ordonnée]]
		for i in range(len(save)):
			for j in range(len(save[0])):  # on regarde les cases une par une pour leur donner une valeur de départ
				typ=save[i][j].getState()
				if typ=="vide" or typ=="eau" or typ=="lave":  # liste non exhaustive des cases que l'on ne peut pas franchir
					  # trv : regarder en fonction des capacité du personnage
					work[i][j].setGraphism(-10)  # mettre une valeur négative sur les cases infranchissable (on met la valeur sur les graphisme)
				else:
					work[i][j].setGraphism(maxi)  # les cases normales ont une valeur maximales, que l'ont fera baisser le plus possible
		for i in listePerso:  # pour chaque personnage
			work[i.getCoord()[0]][i.getCoord()[1]].setGraphism(-10)  # rajouter les positions prises par d'autres personnages
		liste[0][1].append(self.getCoord()[0])
		liste[0][2].append(self.getCoord()[1])  # on ajoute la position du 0 a la liste (de la forme [nb,[x1,xn],[y1,yn]])
		nb=0  # mise a 0 du curseur qui indiquera l'avancement dans ce travail (et le numero des cases que l'on va modifier)
		for j in range (maxi):  # on refait l'operation jusqu'a ce que cela soit impossible d'avoir une case avec un nombre plus grand
			for i in range(len(liste[nb][1])):  # nombre de case a une distance nb du perso
				x=liste[nb][1][i]
				y=liste[nb][2][i]
				if (x+1)<len(save[0]):  # test successif pour éviter les depassements de variables
					dif=self.difTravel(save[x+1][y].getState(),nb+1)
					if save [x+1][y].getGraphism()>dif and (save[x+1][y].getHauteur()-save[x][y].getHauteur()>=-1 and save[x+1][y].getHauteur()-save[x][y].getHauteur()<=1) :  # on test voir si la case a une valeur supérieure à celle possible en faisant une simulation, en récupérant les coordonnées de la case, la valeur actuelle (dans les graphismes), et en comparant avec la valeur voulue (obtenu avec "dif", qui récupère le type de terrain, la difficulté normale (sans les caractéristiques du terrain), et les rassemble avec la difficulté propre au personnage). Puis on regarde si la hauteur n'est pas trop importante (entre -1 et 1 de dif ----->>>>inclu)
						work [x+1] [y].setGraphism(dif)  # en dessous de work
						  # on note les coordonnées des cases pour pouvoir revenir dessus à la prochaine boucle
						liste[dif][1].append(x+1)
						liste[dif][2].append(y)
				  # on recommence avec la case suivante située proche
				if (x-1)>=0:  # test successif pour éviter les depassements de variables
					dif=self.difTravel(save[x-1] [y].getState(),nb+1)
					if save [x-1] [y].getGraphism()>dif and (save[x-1][y].getHauteur()-save[x][y].getHauteur()>=-1 and save[x-1][y].getHauteur()-save[x][y].getHauteur()<=1):
						work [x-1] [y].setGraphism(dif)  # au dessus de work
						liste[dif][1].append(x-1)
						liste[dif][2].append(y)
				  # on recommence avec la case suivante situé proche
				if (y-1)>=0:  # test successif pour éviter les depassements de variables
					dif=self.difTravel(save[x] [y-1].getState(),nb+1)
					if save [x] [y-1].getGraphism()>dif and (save[x][y-1].getHauteur()-save[x][y].getHauteur()>=-1 and save[x][y-1].getHauteur()-save[x][y].getHauteur()<=1):
						work [x] [y-1].setGraphism(dif)  # a gauche de work
						liste[dif][1].append(x)
						liste[dif][2].append(y-1)
				  # on recommence avec la case suivante situé proche
				if (y+1)<len(save):  # test successif pour éviter les depassements de variables
					dif=self.difTravel(save[x] [y+1].getState(),nb+1)
					if save [x] [y+1].getGraphism()>dif and (save[x][y+1].getHauteur()-save[x][y].getHauteur()>=-1 and save[x][y+1].getHauteur()-save[x][y].getHauteur()<=1):
						work [x] [y+1].setGraphism(dif)  # a droite de work
						liste[dif][1].append(x)
						liste[dif][2].append(y+1)
			nb+=1  # on passe a la valeur suivante 
		work[self.getCoord()[0]][self.getCoord()[1]].setGraphism(0)  # remise à 0 de la positon du personnage
		for i in range(len(save)):  # pour chaque case du terrain
			for j in range(len(save[0])):
				if work[i][j].getGraphism()<0:  # si la valeur est negative, alors ce sont des terrains inaccessible
					work[i][j].setGraphism(maxi)  # on leurs met la valeur max
		return(work,maxi)
	
	def rangeTravel(self,nMap,distance,listePerso=[]):
		view=Maps()
		view.contenu=copy.deepcopy(nMap.contenu)
		work=self.testMove(nMap,listePerso)[0]
		for i in range(len(view)):  # pour chaque case du terrain
			for j in range(len(view[0])):
				if work[i][j].getGraphism()<=distance:
					view[i][j].setGraphism(work[i][j].getGraphism())
		if len(listePerso)==0:
			self.printPerso(view)
		else:
			if not(self in listePerso):
				listePerso.append(self)
			printPerso(view,listePerso)
	
	def chemin(self,nMap,x,y,listePerso=[]):
		result=self.testMove(nMap,listePerso)
		move=result[0]
		maxi=result[1]
		if move[x][y].getGraphism()<maxi:
			liste=[[x,y]]
			compt=maxi  # le compt est une sécurité pour ne pas boucler à l'infinie
			while move[x][y].getGraphism()>1 and compt>0:
				if move[x+1][y].getGraphism()<move[x][y].getGraphism():
					x+=1
				elif move[x-1][y].getGraphism()<move[x][y].getGraphism():
					x-=1
				elif move[x][y+1].getGraphism()<move[x][y].getGraphism():
					y+=1
				elif move[x][y-1].getGraphism()<move[x][y].getGraphism():
					y-=1
				liste.append([x,y])
				compt-=1
			return(liste)
		else:
			print("pas de chemin")
			return("none")
	
	def move(self,nMap,screen, x,y,listePerso=[]):
		liste=self.chemin(nMap, x,y ,listePerso)
		if liste!="none":
			oldX=self.getCoord()[0]
			oldY=self.getCoord()[1]
			self.printPerso(nMap,screen)
			for i in range(len(liste)):
				self.setCoord(liste[len(liste)-i-1][0],liste[len(liste)-i-1][1])
				if len(listePerso)==0:
					self.printPerso(nMap,screen)
				else:
					if not(self in listePerso):
						listePerso.append(self)
					printPerso(nMap,screen,listePerso)
		else:
			print("pas de mouvement")


def printPerso(nMap,screen,listePerso):
	data=nMap.printMap(screen, refresh=False)
	screen.getSurface().blit(data[0],data[0].get_rect())
	for i in listePerso:
		position=i.getCoord()  # recuperation de la position des perso
		if position[0]>=0 and position[0]<len(nMap.contenu) and position[1]>=0 and position[1]<len(nMap.contenu[0]):  # pour eviter les dépassement hors tableau
			screen.getSurface().blit(pygame.transform.scale(i.getGraphism(),(data[1],data[2])),(position[0]*data[1],position[1]*data[2]))  # remplacement de l'objet dans le tableau
	pygame.display.flip()


def cloneList(liste):  # retourne une liste qui est une copie de celle en entrée avec une mutabilité étrange (utilisé dans testMove())
	clone=[]
	for i in range (len(liste[0])):
		clone.append((liste[i])[:])
	return clone
