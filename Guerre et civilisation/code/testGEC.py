# -*- coding: utf-8 -*-

from GuerreEtCivilisation import*
from generateurMap import*

screen=Screen(1300,700)#initialisation de GuerreEtCivilisation (resolution de l'affichage)

loadPygameSkin("Data/listeSkinLand.txt")#recuperation des skins dans le fichier dans data

thomas=Perso("moi")#creation d'un personnage 
thomas.setGraphism(pygame.image.load("Data/Perso1_face1.png"))#mise en place du skin
thomas.setOldGraphism("A")
thomas.setCoord(6,7)#positionnement

a=Maps()#une nouvelle map pour faire les tests
a.loadMap("Data/ile.txt")#creation d'une map "ile" (taille:11/11 ; type "ile")

e=Maps()#une map de test supplementaire
e.loadMap("Data/chaine.txt",2)#creation d'une map "montagneuse" (taille:11/11 ; type "chaine")
thomas.printPerso(a,screen)#affichage du perso sur la map1 aux coordonnées de celui ci

print# un retour a la ligne pour la lisibilité
#thomas.testMove(a)#test d'affichage des mouvements

titi=Perso("perso 2")#creation d'un second personnage
titi.setGraphism(pygame.image.load("Data/Perso2_face1.png"))
titi.setOldGraphism("A")
titi.setCoord(3,3)#placement aux coordonnees (3,3)

tata=Perso("perso 3")#creation d'un troisieme perso 
tata.setGraphism(pygame.image.load("Data/Perso3_face1.png"))
tata.setOldGraphism("A")
tata.setCoord(3,5)#placement en position (3,5)

listePerso=[thomas,titi,tata]#liste contenant les persos
printPerso(a,screen,listePerso)#affichage des perso de la liste 'listePerso'
print("listePerso contient les personnages")

z=Maps()#creation de la map de grande taille
z.loadMap("Data/Map1Ile.txt")




