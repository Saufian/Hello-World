# -*- coding: utf-8 -*-
from GuerreEtCivilisation import*

def newMapFile(nomFichier,tailleX,tailleY,fullOf="vide"):
	document=open(nomFichier,'w')#creation du document
	temp=Maps(tailleX,tailleY,fullOf)#creation de map equivalentes
	text=""
	for X in range(len(temp.contenu)):#ajout du comptenu de la map
		for Y in range(len(temp.contenu[0])):
			text+=(str(temp.contenu[Y][X].getState())+" ")#ajout du contenu plus un espace
		text=text[:len(text)-1]#suppression de l'espace en fin de ligne
		text+="\n"#rajout d'un saut de ligne
	text+="fin\n"#fin de la premiere partie
	for i in range(tailleY):#on rajoute le reste du document, en fonction de la complexité max, avec des valeurs neutres
		for j in range(tailleX):
			text+="0.0 "
		text=text[:len(text)-1]#suppression de l'espace en fin de ligne
		text+="\n"#rajout d'un saut de ligne
	text+="fin\n"#la fin de la seconde partie
	document.write(text)
	document.close()


def changeType(doc,screen):
	mapTrv=Maps()
	mapTrv.loadMap(doc,2)
	mapTrv.printMap(screen)
	data=mapTrv.printMap(screen, refresh=False)
	listeTerrain=["vide","lave","plaine","montagne","picInaccessible","eau","foret","spawn","objectif"]
	while True:
		if(pygame.mouse.get_pressed()[0]==1):#clique droit de la souris
			x,y=cases(pygame.mouse.get_pos(),data)#recuperation de la position de la souris
			x1,y1=x/data[1],y/data[2]#mise en relation de la position et des cases
			typeTerrain=listeTerrain.index(mapTrv.contenu[x1][y1].getState())#on recupere la position du nom du terrain dans la liste
			typeTerrain+=1#on passe au terrain suivant
			if typeTerrain>=len(listeTerrain):#on evite de sortir de la liste
				typeTerrain-=len(listeTerrain)#on prend les premiers elements
			mapTrv.contenu[x1][y1].setState(listeTerrain[typeTerrain])#on change le contenu de la case
			mapTrv.contenu[x1][y1].setGraphism("none")#on met à jour les graphismes de la case
			mapTrv.printMap(screen)#on affiche la nouvelle map
			while(pygame.mouse.get_pressed()[0]==1):#temporisation sur la longueur du clic, on regarde si on glisse vers une case proche
				x,y=cases(pygame.mouse.get_pos(),data)#recuperation de la position de la souris
				x2,y2=x/data[1],y/data[2]#mise en relation de la position et des cases
				if (x1!=x2 or y1!=y2):
					mapTrv.contenu[x2][y2].setState(listeTerrain[typeTerrain])#on change le contenu de la case
					mapTrv.contenu[x2][y2].setGraphism("none")#on met à jour les graphismes de la case
					mapTrv.printMap(screen)#on affiche la nouvelle map
					x1,y1=x2,y2#on met la position actuelle du curseur comme position standart
				for event in pygame.event.get():#fais le tour des event pygame
					if event.type == pygame.QUIT: sys.exit()#fermeture si l'on ferme la fenetre
			
		if(pygame.mouse.get_pressed()[2]==1):#meme chose, mais avec le clic gauche, et en decroissant
			x,y=cases(pygame.mouse.get_pos(),data)
			x1,y1=x/data[1],y/data[2]
			typeTerrain=listeTerrain.index(mapTrv.contenu[x1][y1].getState())
			typeTerrain-=1
			if typeTerrain<0:
				typeTerrain+=len(listeTerrain)
			mapTrv.contenu[x1][y1].setState(listeTerrain[typeTerrain])
			mapTrv.contenu[x1][y1].setGraphism("none")
			mapTrv.printMap(screen)
			while(pygame.mouse.get_pressed()[2]==1):#temporisation sur la longueur du clic, on regarde si on glisse vers une case proche
				x,y=cases(pygame.mouse.get_pos(),data)#recuperation de la position de la souris
				x2,y2=x/data[1],y/data[2]#mise en relation de la position et des cases
				if (x1!=x2 or y1!=y2):
					mapTrv.contenu[x2][y2].setState(listeTerrain[typeTerrain])#on change le contenu de la case
					mapTrv.contenu[x2][y2].setGraphism("none")#on met à jour les graphismes de la case
					mapTrv.printMap(screen)#on affiche la nouvelle map
					x1,y1=x2,y2#on met la position actuelle du curseur comme position standart
				for event in pygame.event.get():#fais le tour des event pygame
					if event.type == pygame.QUIT: sys.exit()#fermeture si l'on ferme la fenetre
		
		if(pygame.mouse.get_pressed()[1]==1):#clique central de la souris
			document = open(doc,"r")#ouverture du document en lecture pour recuperé les données importantes
			text=""
			finText=""
			partie=1#on commence toujours par le debut (premiere partie du texte)
			for ligne in document:
				if ligne=="fin\n":#on compte les partie, delimité par les mots "fin"
					partie += 1
				if partie>1:#on evite la premiere partie
					finText+=ligne#on recupere la ligne
			document.close()#on oublie pas de fermer le doc
			document = open(doc,"w")#ouverture du document en ecriture
			for X in range(len(mapTrv.contenu)):
				for Y in range(len(mapTrv.contenu[0])):
					text+=(str(mapTrv.contenu[Y][X].getState())+" ")#ajout du contenu plus un espace
				text=text[:len(text)-1]#suppression de l'espace en fin de ligne
				text+="\n"#rajout d'un saut de ligne
			text+=finText#et on remet la fin du fichier
			document.write(text)
			document.close()
			while(pygame.mouse.get_pressed()[1]==1):#temporisation sur la longueur du clic
					for event in pygame.event.get():#fais le tour des event pygame
						if event.type == pygame.QUIT: sys.exit()#fermeture si l'on ferme la fenetre
		
		for event in pygame.event.get():#fais le tour des event pygame
			if event.type == pygame.QUIT: sys.exit()#fermeture si l'on ferme la fenetre


def changeDenivele(doc,screen):
	mapTrv=Maps()
	mapTrv.loadMap(doc,2)
	mapTrv.printMap(screen)
	data=mapTrv.printMap(screen,refresh=False)#recuperation des données de la map
	while True:
		if(pygame.mouse.get_pressed()[0]==1):#clique droit de la souris
			x,y=cases(pygame.mouse.get_pos(),data)#recuperation de la position de la souris
			x1,y1=x/data[1],y/data[2]#mise en relation de la position et des cases
			mapTrv.contenu[x1][y1].setHauteur(mapTrv.contenu[x1][y1].getHauteur()+1)#augmentation de la hauteur
			print(mapTrv.contenu[x1][y1].getHauteur())#controle sur le terminal
			while(pygame.mouse.get_pressed()[0]==1):#temporisation sur la longueur du clic
				for event in pygame.event.get():#fais le tour des event pygame
					if event.type == pygame.QUIT: sys.exit()#fermeture si l'on ferme la fenetre
		
		if(pygame.mouse.get_pressed()[2]==1):#clique gauche de la souris
			x,y=cases(pygame.mouse.get_pos(),data)#recuperation de la position de la souris
			x1,y1=x/data[1],y/data[2]#mise en relation de la position et des cases
			mapTrv.contenu[x1][y1].setHauteur(mapTrv.contenu[x1][y1].getHauteur()-1)#diminution de la hauteur
			print(mapTrv.contenu[x1][y1].getHauteur())#controle terminal
			while(pygame.mouse.get_pressed()[2]==1):#temporisation sur la longueur du clic
				for event in pygame.event.get():#fais le tour des event pygame
					if event.type == pygame.QUIT: sys.exit()#fermeture si l'on ferme la fenetre
		
		if(pygame.mouse.get_pressed()[1]==1):#clique central de la souris
			document = open(doc,"r")#ouverture du document en lecture pour recuperé les données importantes
			text=""
			finText=""
			partie=1#on commence toujours par le debut (premiere partie du texte)
			for ligne in document:
				if ligne=="fin\n":#on compte les partie, delimité par les mots "fin"
					partie += 1
				if partie==1:
					text+=ligne#on recupere la ligne
				if partie>2:#on evite la seconde partie
					finText+=ligne#on recupere la ligne
			text+="fin\n"#le caractere de fin de la premiere serie de données
			document.close()#on oublie pas de fermer le doc
			document = open(doc,"w")#ouverture du document en ecriture
			for X in range(len(mapTrv.contenu)):
				for Y in range(len(mapTrv.contenu[0])):
					text+=(str(mapTrv.contenu[Y][X].getHauteur())+" ")#ajout du contenu plus un espace
				text=text[:len(text)-1]#suppression de l'espace en fin de ligne
				text+="\n"#rajout d'un saut de ligne
			text+=finText#et on remet la fin du fichier
			document.write(text)

			document.close()
			while(pygame.mouse.get_pressed()[1]==1):#temporisation sur la longueur du clic
					for event in pygame.event.get():#fais le tour des event pygame
						if event.type == pygame.QUIT: sys.exit()#fermeture si l'on ferme la fenetre
		
		for event in pygame.event.get():#fais le tour des event pygame
			if event.type == pygame.QUIT: sys.exit()#fermeture si l'on ferme la fenetre
