# -*- coding: utf-8 -*-

import map
import gec_motor
import pygame
import sys


def new_map_file(nom_fichier, taillex, tailley, full_of="vide"):
    document = open(nom_fichier, 'w')  # création du document
    temp = map.Maps(taillex, tailley, full_of)  # creation de map équivalentes
    text = ""
    for X in range(len(temp.contenu)):  # ajout du comptenu de la map
        for Y in range(len(temp.contenu[0])):
            text += (str(temp.contenu[Y][X].state) + " ")  # ajout du contenu plus un espace
        text = text[: len(text) - 1]  # suppression de l'espace en fin de ligne
        text += "\n"  # rajout d'un saut de ligne
    text += "fin\n"  # fin de la première partie
    for i in range(tailley):
        # on rajoute le reste du document, en fonction de la complexité max, avec des valeurs neutres
        for j in range(taillex):
            text += "0.0 "
        text = text[: len(text) - 1]  # suppression de l'espace en fin de ligne
        text += "\n"  # rajout d'un saut de ligne
    text += "fin\n"  # la fin de la seconde partie
    document.write(text)
    document.close()
    return nom_fichier


def change_type(doc, screen):  # TODO : mettre en place une securité pour éviter un depassement du terrain
    work_map = map.Maps()
    work_map.load_map(doc, 1)
    work_map.print_map(screen)
    data = work_map.print_map(screen, refresh=False)
    liste_terrain = ["vide", "lave", "plaine", "montagne", "picInaccessible", "eau", "foret", "spawn", "objectif"]
    while True:
        if pygame.mouse.get_pressed()[0] == 1:  # clique gauche de la souris = changement de terrain (croissant)
            pos_mouse = pygame.mouse.get_pos()
            pos_mouse = (pos_mouse[0]-screen.pos_x, pos_mouse[1]-screen.pos_y)
            x, y = gec_motor.cases(pos_mouse, data)  # récupération de la position de la souris
            x1, y1 = x // data[1], y // data[2]  # mise en relation de la position et des cases
            type_terrain = liste_terrain.index(work_map.contenu[x1][y1].state)
              # on recupere la position du nom du terrain dans la liste
            type_terrain += 1  # on passe au terrain suivant
            if type_terrain >= len(liste_terrain):  # on evite de sortir de la liste
                type_terrain -= len(liste_terrain)  # on prend les premiers elements
            work_map.contenu[x1][y1].set_state(liste_terrain[type_terrain])  # on change le contenu de la case
            work_map.contenu[x1][y1].set_graphism(None)  # on met à jour les graphismes de la case
            work_map.contenu[x1][y1].upgrade_graphism()
            work_map.print_map(screen)  # on affiche la nouvelle map
            while pygame.mouse.get_pressed()[0] == 1:
                # temporisation sur la longueur du clic, on regarde si on glisse vers une case proche
                pos_mouse = pygame.mouse.get_pos()
                pos_mouse = (pos_mouse[0]-screen.pos_x, pos_mouse[1]-screen.pos_y)
                x, y = gec_motor.cases(pos_mouse, data)  # récupération de la position de la souris
                x2, y2 = x // data[1], y // data[2]  # mise en relation de la position et des cases
                if x1 != x2 or y1 != y2:
                    work_map.contenu[x2][y2].set_state(liste_terrain[type_terrain])  # on change le contenu de la case
                    work_map.contenu[x2][y2].set_graphism(None)  # on met à jour les graphismes de la case
                    work_map.print_map(screen)  # on affiche la nouvelle map
                    x1, y1 = x2, y2  # on met la position actuelle du curseur comme position standard
                for event in pygame.event.get():  # fais le tour des event pygame
                    if event.type == pygame.QUIT:
                        sys.exit()  # fermeture si l'on ferme la fenêtre

        if pygame.mouse.get_pressed()[2] == 1:  # meme chose, mais avec le clic droit, et en decroissant
            pos_mouse = pygame.mouse.get_pos()
            pos_mouse = (pos_mouse[0]-screen.pos_x, pos_mouse[1]-screen.pos_y)
            x, y = gec_motor.cases(pos_mouse, data)  # récupération de la position de la souris
            x1, y1 = x // data[1], y // data[2]
            type_terrain = liste_terrain.index(work_map.contenu[x1][y1].state)
            type_terrain -= 1
            if type_terrain < 0:
                type_terrain += len(liste_terrain)
            work_map.contenu[x1][y1].set_state(liste_terrain[type_terrain])
            work_map.contenu[x1][y1].set_graphism(None)
            work_map.print_map(screen)
            while pygame.mouse.get_pressed()[2] == 1:
              # temporisation sur la longueur du clic, on regarde si on glisse vers une case proche
                pos_mouse = pygame.mouse.get_pos()
                pos_mouse = (pos_mouse[0]-screen.pos_x, pos_mouse[1]-screen.pos_y)
                x, y = gec_motor.cases(pos_mouse, data)  # récupération de la position de la souris
                x2, y2 = x // data[1], y // data[2]  # mise en relation de la position et des cases
                if x1 != x2 or y1 != y2:
                    work_map.contenu[x2][y2].set_state(liste_terrain[type_terrain])  # on change le contenu de la case
                    work_map.contenu[x2][y2].set_graphism(None)  # on met à jour les graphismes de la case
                    work_map.print_map(screen)  # on affiche la nouvelle map
                    x1, y1 = x2, y2  # on met la position actuelle du curseur comme position standard
                for event in pygame.event.get():  # fais le tour des event pygame
                    if event.type == pygame.QUIT:
                        sys.exit()  # fermeture si l'on ferme la fenêtre

        if pygame.mouse.get_pressed()[1] == 1:  # clique central de la souris = sauvegarde du document
            document = open(doc, "r")  # ouverture du document en lecture pour récupéré les données importantes
            text = ""
            text_end = ""
            partie = 1  # on commence toujours par le debut (premiere partie du texte)
            for ligne in document:
                if ligne == "fin\n":  # on compte les partie, delimité par les mots "fin"
                    partie += 1
                if partie > 1:  # on évite la première partie
                    text_end += ligne  # on récupère la ligne
            document.close()  # on oublie pas de fermer le doc
            document = open(doc, "w")  # ouverture du document en ecriture
            for X in range(len(work_map.contenu)):
                for Y in range(len(work_map.contenu[0])):
                    text += (str(work_map.contenu[Y][X].state) + " ")  # ajout du contenu plus un espace
                text = text[: len(text) - 1]  # suppression de l'espace en fin de ligne
                text += "\n"  # rajout d'un saut de ligne
            text += text_end  # et on remet la fin du fichier
            document.write(text)
            document.close()
            while pygame.mouse.get_pressed()[1] == 1:  # temporisation sur la longueur du clic
                for event in pygame.event.get():  # fais le tour des event pygame
                    if event.type == pygame.QUIT:
                        sys.exit()  # fermeture si l'on ferme la fenêtre

        for event in pygame.event.get():  # fais le tour des event pygame
            if event.type == pygame.QUIT:
                sys.exit()  # fermeture si l'on ferme la fenêtre


def change_denivele(doc, screen):
    work_map = map.Maps()
    work_map.load_map(doc, 2)
    work_map.print_map(screen)
    data = work_map.print_map(screen, refresh=False)  # recuperation des données de la map
    while True:
        if pygame.mouse.get_pressed()[0] == 1:  # clique droit de la souris
            x, y = gec_motor.cases(pygame.mouse.get_pos(), data)  # récupération de la position de la souris
            x1, y1 = x // data[1], y // data[2]  # mise en relation de la position et des cases
            work_map.contenu[x1][y1].set_hauteur(work_map.contenu[x1][y1].hauteur + 1)
                # augmentation de la hauteur
            print(work_map.contenu[x1][y1].hauteur)  # controle sur le terminal
            while pygame.mouse.get_pressed()[0] == 1:  # temporisation sur la longueur du clic
                for event in pygame.event.get():  # fais le tour des event pygame
                    if event.type == pygame.QUIT:
                        sys.exit()  # fermeture si l'on ferme la fenêtre

        if pygame.mouse.get_pressed()[2] == 1:  # clique gauche de la souris
            x, y = gec_motor.cases(pygame.mouse.get_pos(), data)  # récupération de la position de la souris
            x1, y1 = x // data[1], y // data[2]  # mise en relation de la position et des cases
            work_map.contenu[x1][y1].set_hauteur(work_map.contenu[x1][y1].hauteur - 1)  # diminution de la hauteur
            print(work_map.contenu[x1][y1].hauteur)  # contrôle terminal
            while pygame.mouse.get_pressed()[2] == 1:  # temporisation sur la longueur du clic
                for event in pygame.event.get():  # fais le tour des event pygame
                    if event.type == pygame.QUIT:
                        sys.exit()  # fermeture si l'on ferme la fenêtre

        if pygame.mouse.get_pressed()[1] == 1:  # clique central de la souris
            document = open(doc, "r")  # ouverture du document en lecture pour récupéré les données importantes
            text = ""
            text_end = ""
            partie = 1  # on commence toujours par le debut (premiere partie du texte)
            for ligne in document:
                if ligne == "fin\n":  # on compte les partie, délimité par les mots "fin"
                    partie += 1
                if partie == 1:
                    text += ligne  # on récupère la ligne
                if partie > 2:  # on évite la seconde partie
                    text_end += ligne  # on récupère la ligne
            text += "fin\n"  # le caractere de fin de la première série de données
            document.close()  # on oublie pas de fermer le doc
            document = open(doc, "w")  # ouverture du document en ecriture
            for X in range(len(work_map.contenu)):
                for Y in range(len(work_map.contenu[0])):
                    text += (str(work_map.contenu[Y][X].hauteur) + " ")  # ajout du contenu plus un espace
                text = text[: len(text) - 1]  # suppression de l'espace en fin de ligne
                text += "\n"  # rajout d'un saut de ligne
            text += text_end  # et on remet la fin du fichier
            document.write(text)

            document.close()
            while pygame.mouse.get_pressed()[1] == 1:  # temporisation sur la longueur du clic
                for event in pygame.event.get():  # fais le tour des event pygame
                    if event.type == pygame.QUIT:
                        sys.exit()  # fermeture si l'on ferme la fenêtre

        for event in pygame.event.get():  # fais le tour des event pygame
            if event.type == pygame.QUIT:
                sys.exit()  # fermeture si l'on ferme la fenêtre
