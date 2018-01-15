# -*- coding: utf-8 -*-

import pygame

class Land:# objet Land, qui compose les cartes de jeu.
	def __init__(self, ID):#creation de map, avec un type de map pour l'identification et pour l'affichage si pas de graphisme spéciaux définis
		self.state = ID
		self.graphism="none"#pas de graphisme par défaut
		self.oldGraphism="none"#pas de graphisme par défaut pour l'affichage dans le terminal
		self.hauteur = 0#correspond a la hauteur de l'élément. Un personnage basique ne peut pas monter 1 de hauteur
		self.spe=[]#ajoute des caracteristiques speciales
		
	def setState(self,ID):#changement du type de terrain
		self.state=ID
		
	def getState(self):#retourne le type actuel du terrain
		return self.state
	
	def setSpe(self,typ):#met en place les caracteristiques speciales
		if not(typ in self.spe):#verification de la non presence (pas de doublon)
			self.spe.append(typ)
	
	def getSpe(self,typ):#renvoi "True" si le terrain a la caracteristique speciale typ
		return(typ in self.spe)
	
	def setName(self,ID):#possibilité de donner un nom au terrain
		self.name=ID
		
	def getName(self):#retourne le nom du terrain
		return self.name
	
	def setHauteur(self,nb):
		self.hauteur=nb
		self.upgradeGraphism()# mise à jour des graphismes
	
	def getHauteur(self):
		return self.hauteur
	
	def setGraphism(self, graph):#changement des graphisme pour ce terrain
		self.graphism=graph
	#trv  ameliorer le code ci-dessous
	def getGraphism(self):#renvoi les graphismes pour l'affichage de l'objet : la valeur associé au type de terrain ( par defaut )
				# ou une apparence bien spécifique sous la forme de Str
		if self.graphism!="none":#si les graphismes ont deja été initialisé
			return self.graphism
		else:
			self.graphism=self.upgradeGraphism()#sinon definire les parametres
			return(self.graphism)
	
	def upgradeGraphism(self):
		skinFinal=pygame.Surface((32,32))#taille d'une image du terrain (correspond a la resolution d'une case)
		for i in LoadSkin.listeLoad:#recuperation des differents graphismes
			if self.state==i.ID:#si le nom de l'etat du terrain correspond avec le nom du skin
				skinFinal.blit(i.pygameImage,(0,0))#recuperer la surface (de pygame) correspondante
				#  return self.graphism#retourner les bons graphismes
				for j in LoadSkin.listeLoad:#verification que les graphismes pour representer la hauteur sont definis
					if "denivele"==j.ID:
						for i in range(int(self.hauteur)):#on fait apparaitre {hauteur} fois les graphismes pour montrer le denivelé
							skinFinal.blit(j.pygameImage,(0,32-((self.hauteur+1)*8)))#positionnement du rajout
				return skinFinal
		return("ERROR")
	
	
	def getOldGraphism(self):#renvoi les graphismes pour l'affichage dans le terminal pour le mode developpeur de l'objet : la valeur associé au type de terrain ( par defaut )
				# ou une apparence bien spécifique sous la forme de Str
		if self.oldGraphism!="none":
			return self.oldGraphism
		for i in LoadSkin.listeLoad:
			if self.state==i.ID:
				self.oldGraphism= i.oldSkin
				return self.oldGraphism
		return("ERROR")
	


class Maps:
	lastMapPrint=[[],[]]
	def __init__(self,xmax=0,ymax=0,typ="vide"):#creation d'une map de taille "xmax","ymax", stocké dans la liste "name", rempli de Land de type "typ"
		self.contenu=[]
		for x in range (xmax):
			self.contenu.append([])
			for y in range (ymax):
				self.contenu[x].append(Land(typ))
	
	
	def createMap(self,xmax,ymax,typ="vide"):#creation d'une map de taille "xmax","ymax", stocké dans la liste "name", rempli de Land de type "typ"
		del self.contenu[:]
		for x in range (xmax):
			self.contenu.append([])
			for y in range (ymax):
				self.contenu[x].append(Land(typ))


	def printOldMap(self,x=0,y=0,largeur=-1,hauteur=-1):
		if largeur==-1 or largeur>len(self.contenu):
			largeur=len(self.contenu)
		if hauteur==-1 or hauteur>len(self.contenu[0]):
			hauteur=len(self.contenu[0])
		if x<0:
			x=0
		if y<0:
			y=0
		if x>=largeur:
			if x<1:
				largeur+=(x-largeur)+1
			else:
				x-=(x-largeur)+1
		if y>=hauteur:
			if y<1:
				hauteur+=(y-hauteur)+1
			else:
				y-=(y-hauteur)+1
		for i in range (y,hauteur):
			mapAffiche=[]
			for j in range (x,largeur):
				#if type(mapTarget[j][i])==type(""):#Si c'est directement un caractère
				#	mapAffiche.append(mapTarget[j][i])
				#else:
				mapAffiche.append(self.contenu[j][i].getOldGraphism())#tran
			print(mapAffiche)


	def printMap(self,screen,x=0,y=0,largeur=-1,hauteur=-1,refresh=True):
		if largeur==-1 or largeur>len(self.contenu):
			largeur=len(self.contenu)
		if hauteur==-1 or hauteur>len(self.contenu[0]):
			hauteur=len(self.contenu[0])
		if x<0:
			x=0
		if y<0:
			y=0
		if x>=largeur:
			if x<1:
				largeur+=(x-largeur)+1
			else:
				x-=(x-largeur)+1
		if y>=hauteur:
			if y<1:
				hauteur+=(y-hauteur)+1
			else:
				y-=(y-hauteur)+1
		
		#trv : mette en pace un systeme de sauvegarde qui utilise une memoire des 10 derniers affichage(en cas de réutilisation)
		#if [x,y,largeur,hauteur] in Maps.lastMapPrint[0]:
		#	ecran=Maps.lastMapPrint[1][Maps.lastMapPrint[0].index([x,y,largeur,hauteur])]#(1180 , 630)
		#	ecran=pygame.transform.scale(ecran,(1180,630))
		#	screen.getSurface().blit(ecran,(0,0))
		#	pygame.display.flip()
		#else:
		for i in range (y,hauteur):
			for j in range (x,largeur):
				skin=self.contenu[j][i].getGraphism()
				skin=pygame.transform.scale(skin,(screen.getSize()[0]//(largeur-x),screen.getSize()[1]//(hauteur-y)))
				screen.getSurface().blit(skin, (j*(screen.getSize()[0]//(largeur-x)),i*(screen.getSize()[1]//(hauteur-y))))
		#lastMapUse([x,y,largeur,hauteur],screen.getSurface())
		if refresh:
		 	pygame.display.flip()
		else:
			return(screen.getSurface(),screen.getSize()[0]//(largeur-x),screen.getSize()[1]//(hauteur-y))
	
	def loadMap(self,doc,complexite=1):#complexite correspond au niveau de detail de la map
		data=chargeMot(doc,1)#data contient toutes les informations sur la map
		del self.contenu[:]#on vide la map precedente pour être sur de ne pas réécrire dessus
		for x in range (len(data[0])):
			self.contenu.append([])
			for y in range (len(data)):
				self.contenu[x].append(Land(data[y][x]))#on relie chaque info de data avec les objets adapté
		if complexite>1:#obligatoire de faire du cas par cas
			if complexite>=2:#detail sur l'altitude 
				data=chargeMot(doc,2)
				for x in range (len(data[0])):
					for y in range (len(data)):
						self.contenu[y][x].setHauteur(float(data[x][y]))#attention a l'ordre du contenu dans les coordonnées
			
	
	def refresh(self):
		for i in range(len(self.contenu)):
			for j in range(len(self.contenu[i])):
				self.contenu[i][j].setGraphism("none")


def lastMapUse(data,screen):#fonction non finalisé, doit pouvoir mettre en memoire les informaion des dernieres map affichées, pour accelerer le processus
	Maps.lastMapPrint[0].append(data)
	Maps.lastMapPrint[1].append(screen.getSurface())
	while len(Maps.lastMapPrint[0])>10:
		for i in range (1,len(Maps.lastMapPrint[0])):
			Maps.lastMapPrint[0][i-1]=Maps.lastMapPrint[0][i]
			Maps.lastMapPrint[1][i-1]=Maps.lastMapPrint[1][i]
		del(Maps.lastMapPrint[0][len(Maps.lastMapPrint[0])-1])
		del(Maps.lastMapPrint[1][len(Maps.lastMapPrint[1])-1])


def chargeMot(doc,complexite=1):#fonction d'extraction de données dans un DOCument, jusqu'à trouver une ligne avec seulement le mot "fin" [complexite] fois
	file=open(doc,'r')#on ouvre le doc en mode lecture
	for i in range(complexite):
		retour=[]#on ne capte ainsi que le contenu du [complexite] bloc finissant par "fin"
		ligne=file.readline()#attention, le retour a la ligne est aussi recuperé
		ligne=ligne[:len(ligne)-1]#on supprime le retour a la ligne.
		while ligne!="fin":#on prend toutes les lignes jusqu'à trouver le mot "fin"
			retour.append(ligne.split(" ")[:])#on separe chaque mot de la ligne
			ligne=file.readline()#on prend la ligne suivante
			ligne=ligne[:len(ligne)-1]#on supprime le retour a la ligne de la nouvelle ligne
	file.close()#on oublie pas de fermer le doc
	return(retour)


def loadPygameSkin(doc):#fonction principale dans le chargement des images : va charger toutes les images dont les adresses sont contenus dans le DOCument.
#le document doit etre de la forme : [nom du skin] [adresse du skin] [symbole pour le debugger(pas obligatoire)]
	data=chargeMot(doc)
	for i in data:#pour chaque skin, creer un objet de LoadSkin
		load=LoadSkin(i[0])#associe le nom
		if len(i)==2:#pas de troisieme entrée
			load.setSkin(i[1])
		elif len(i)==3:#mettre aussi en place le symbole pour le debug
			load.setSkin(i[1],i[2])
		

class LoadSkin:
	listeLoad=[]#contient les objets avec les skins
	def __init__(self,ID,frame=0):
		self.ID=ID#nom du skin
		self.frame=frame#inutilisé pour l'instant
		self.pygameSkinLocation=None#contiendra l'adresse du skin
		self.pygameImage=None#contiendra directement la surface associé à l'adresse
		self.oldSkin=None#contiendra le graphisme associé au nom pour passer en mode débuggage (pas nescessaire dans tous les cas)
		LoadSkin.listeLoad.append(self)#ajoute chaque objet à la liste
	
	def setSkin(self,pygameSkinLocation,oldSkin=None):#met en place les graphismes de cet objet
		self.pygameSkinLocation=pygameSkinLocation#adresse
		self.pygameImage=pygame.image.load(pygameSkinLocation).convert()#suface associée
		self.oldSkin=oldSkin#skin de debug


