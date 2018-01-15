# -*- coding: utf-8 -*-

from perso import*
#from __future__ import division
from map import*
import sys, pygame

pygame.init()#initialisation de Pygame


class Screen:#objet permettant de superposer des fenetres de taille variable. 
	def __init__ (self,screenWidth,screenHeight):#creation d'une nouvelle fenetre
		self.width=screenWidth
		self.height=screenHeight
		size=screenWidth,screenHeight
		self.surface = pygame.display.set_mode(size)
	def getSize(self):#retourne la taille de l'objet
		return(self.width,self.height)
	def getSurface(self):#retourne le pygame.surface voulu
		return self.surface
	def setSurface(self,newSurface):
		self.surface = newSurface




def loopBase():#fonction de base, attendant juste la fermeture
	while 1:#boucle de base
		for event in pygame.event.get():#evenement python
			if event.type == pygame.QUIT: sys.exit()#exit

def cases(t,data):#fonction pour placer les images commes si elles étaient dans un tableau (repartition dans des cases)
	x,y=t
	return((x//data[1])*data[1],(y//data[2])*data[2])

def game1(maps,listePerso,screen):#première fonction de jeu, 3 perso(thomas,tata,titi) qui vont là où l'on clique
	data=maps.printMap(screen.getSurface(),screen.getSize()[0],screen.getSize()[1],refresh=False)#recuperation des données du terrain
	while True:
		if(pygame.mouse.get_pressed()[0]==1):
			x,y=cases(pygame.mouse.get_pos(),data)
			thomas.move(maps,screen.getSize()[0],screen.getSize()[1],x/data[1],y/data[2],listePerso)
		if(pygame.mouse.get_pressed()[2]==1):
			x,y=cases(pygame.mouse.get_pos(),data)
			tata.move(maps,screen.getSize()[0],screen.getSize()[1],x/data[1],y/data[2],listePerso)
		if(pygame.mouse.get_pressed()[1]==1):
			x,y=cases(pygame.mouse.get_pos(),data)
			titi.move(maps,screen.getSize()[0],screen.getSize()[1],x/data[1],y/data[2],listePerso)
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

def wIAm(x,y,listePerso):#retrouve le personnage au coordonnée donnée (who I am?)
	for i in listePerso:#pour chaque joueur:
		if i.getCoord()==[x,y]:#regarde si les coordonnées correspondent
			return i#renvoi le personnage
	return(None)#ne retourne rien

def game(maps,listePerso,screen):#fonction de jeu actuel, sur la map, avec la listePerso, et sur l'ecran donnés
	posPerso=0#position du personnage selectionné
	focus=None#contient le personnage selectionné, ou none sinon
	data=maps.printMap(screen,refresh=False)#recuperation des données de la map
	printPerso(maps,screen,listePerso)#affichage des perso
	while True:
		if(pygame.mouse.get_pressed()[0]==1):#clique droit de la souris
			if focus==None:#si pas de personnages selectionés
				x,y=cases(pygame.mouse.get_pos(),data)#recuperation de la position de la souris
				x1,y1=x/data[1],y/data[2]#mise en relation de la position et des cases
				focus=wIAm(x1,y1,listePerso)#identification d'un personnage, et mise dans le focus
				if focus in listePerso:
					posPerso=x1,y1#position initiale du personnage (en case)
			else :#si il y a un personnage selectionné
				x,y=cases(pygame.mouse.get_pos(),data)#données de la souris
				x1,y1=x/data[1],y/data[2]#case pour la souris
				if posPerso!=(x1,y1):#si la position du perso est différente
					focus.move(maps,screen,x/data[1],y/data[2],listePerso)#deplace le personnage dans une nouvelle case
					focus=None
		for event in pygame.event.get():#fais le tour des event pygame
			if event.type == pygame.QUIT: sys.exit()#fermeture si l'on ferme la fenetre


