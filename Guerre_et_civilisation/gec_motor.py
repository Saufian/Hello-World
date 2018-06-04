# -*- coding: utf-8 -*-

from perso import *
# from __future__ import division
import sys
import pygame

pygame.init()  # Pygame initialisation


class Screen:  # objet permettant de superposer des fenetres de taille variable dans la première fenetre créé (main)
    source = ""
    main = None  # à définir lors de l'initialisation (la premiere fenetre créé par défaut)
    list_screen = []  # liste de tous les objets

    def __init__(self, pos_x, pos_y, screen_width, screen_height, prior=0, type_screen="default", change_param=None):
        if change_param is None:
            change_param = []
        # creation d'une nouvelle fenetre
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = screen_width
        self.height = screen_height
        size = screen_width, screen_height
        self.surface = pygame.Surface(size)
        self.param = [["closeButton", "backgroundColor", "move", "transparent", "changeSized"],
                      [False, (0, 0, 0), False, False, False]]  # param type default
        self.load_param(type_screen)
        for i in change_param:
            temp = i.split(" ")
            if temp[0] in self.param[0]:
                value = temp[-1][:-1]  # on va interpréter les valeurs dans temp
                if value == "False":
                    value = False
                elif value == "True":
                    value = True
                self.param[1][self.param[0].index(temp[0])] = value
        # on regle maintenant les problèmes de priorités dans l'affichage
        self.prior = prior
        if self.prior == 0:
            Screen.list_screen.append(self)
            self.prior = Screen.list_screen[-1].prior+1
        if self.prior == -1:
            Screen.list_screen.reverse()
            Screen.list_screen.append(self)
            Screen.list_screen.reverse()
            self.prior = 0
            for i in range(1, len(Screen.list_screen)):
                Screen.list_screen[i].prior = i

    def load_param(self, type_screen="default"):  # type_screen correspond au réglage déjà mis dans Screen.source
        doc = open(Screen.source, 'r')
        data = []
        indata = False
        for ligne in doc:  # on parcours le document et on extrait les info
            if ligne == "fin\n":
                indata = False  # fin de la partie demandé, on arrete la lecture
            if indata:
                data.append(ligne)
            if ligne == type_screen + "\n":  # on attend le début de la description du type demandé avant de lire
                indata = True
        doc.close()
        for i in data:
            temp = i.split(" ")
            if temp[0] in self.param[0]:  # on va remplir la liste des parametres
                value = temp[-1][:-1]  # on va interpréter les valeurs dans temp
                if value == "False":
                    value = False
                elif value == "True":
                    value = True
                elif temp[0] == "backgroundColor":
                    travail = []
                    for j in value[1:-1].split(","):
                        travail.append(int(j))
                    value = (travail[0], travail[1], travail[2])
                self.param[1][self.param[0].index(temp[0])] = value  # on enleve le caractère de fin de ligne

    def get_size(self):  # retourne la taille de l'objet (sous forme de tuple)
        return self.width, self.height

    def set_surface(self, new_surface):  # set the surface on the screen
        self.surface = new_surface

    def get_param(self, name):  # renvoi un boolean correspondant à la possession du paramétre
        if name in self.param[0]:
            return self.param[1][self.param[0].index(name)]
        else:
            return None


def condense_screen(liste_screen=Screen.list_screen):  # affiche les differents sous ecran dans la fenetre principale
    for i in liste_screen:  # pour chaque sous-écran
        Screen.main.blit(i.surface, (i.pos_x, i.pos_y))  # affiche le sous-ecran sur l'écran principal
    return Screen.main  # retourne l'écran principal formé des sous-écran


def cases(t, data):
    # fonction pour placer les images commes si elles étaient dans un tableau (repartition dans des cases)
    x, y = t
    return (x // data[1]) * data[1], (y // data[2]) * data[2]


def wiam(x, y, liste_perso):  # retrouve le personnage au coordonnée donnée (who I am?)
    for i in liste_perso:  # pour chaque joueur:
        if i.coord == [x, y]:  # regarde si les coordonnées correspondent
            return i  # renvoi le personnage
    return None  # nothing return


def game(maps, liste_perso, screen, boucle=True):  # jeu, sur la map, avec la liste_perso, et sur l'ecran donnés
    pos_perso = 0  # position du personnage selectionné
    focus = None  # contient le personnage selectionné, ou none sinon
    data = maps.print_map(screen, refresh=False)  # recuperation des données de la map
    print_perso(maps, screen, liste_perso)  # affichage des perso
    loop = True
    while loop:
        pygame.time.wait(50)
        for event in pygame.event.get():  # fais le tour des event pygame
            if event.type == pygame.QUIT:
                sys.exit()  # fermeture si l'on ferme la fenetre
        if pygame.mouse.get_pressed()[0] == 1:  # clique droit de la souris
            while pygame.mouse.get_pressed()[0] == 1:
                for event in pygame.event.get():  # fais le tour des event pygame
                    if event.type == pygame.QUIT:
                        sys.exit()  # fermeture si l'on ferme la fenêtre
            pos_mouse = pygame.mouse.get_pos()
            pos_mouse = (pos_mouse[0]-screen.pos_x, pos_mouse[1]-screen.pos_y)
            x, y = cases(pos_mouse, data)  # recuperation de la position de la souris
            x1, y1 = x // data[1], y // data[2]  # mise en relation de la position et des cases
            if focus is None:  # si pas de personnages selectionés
                focus = wiam(x1, y1, liste_perso)  # identification d'un personnage, et mise dans le focus
                if focus in liste_perso:
                    pos_perso = x1, y1  # position initiale du personnage (en case)
            else:  # si il y a un personnage selectionné
                if pos_perso != (x1, y1):  # si la position du perso est différente
                    focus.move(maps, screen, x1, y1, liste_perso)
                    # deplace le personnage dans une nouvelle case
                    focus = None
        if focus is None:
            loop = boucle  # gestion de la boucle while : ne pas passer à la suite si un personnage est séléctionné


def what_screen(x, y, liste_screen):
    selection_viable = []
    for i in liste_screen:
        if i.pos_x <= x <= i.pos_x+i.width and i.pos_y <= y <= i.pos_y+i.height:
            selection_viable.append(i)
    if len(selection_viable) == 0:
        print("erreur screen")
    maxi_prior = selection_viable[0].prior
    sol = selection_viable[0]
    for i in selection_viable:
        if i.prior > maxi_prior:
            sol = i
            maxi_prior = i.prior
    return sol


def test_keyboard(test):  # test correspond au caractere que l'on doit regarder --> renvoi True si la touche est appuiée
    enter = pygame.key.get_pressed()
    enter = [i for i in enter]  # on passe de tuple a liste
    enter[300] = 0  # on enleve le {verr num}
    charact = ""
    if 1 in enter:
        charact = pygame.key.name(enter.index(1))  # on laisse pygame identifier la touche
    return charact == test  # comparaison avec la touche demandé


def deplace_screen(liste_screen, x, y):
    screen_on = what_screen(x, y, liste_screen)  # on trouve l'ecran sur lequel on se trouve
    x_cursor = x - screen_on.pos_x
    y_cursor = y - screen_on.pos_y
    if screen_on.get_param("move"):  # si l'on peut faire bouger l'écran
        while pygame.mouse.get_pressed()[0] == 1:  # on attend que le bouton soit relaché
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            x, y = pygame.mouse.get_pos()  # on récupère la position du curseur
        screen_on.pos_x, screen_on.pos_y = x - x_cursor, y - y_cursor  # on place l'écran à la position du curseur


def game_window(arg):  # fonction de jeu actuel, map choisi, avec les perso, et gestion d'ecran
    # arg de la forme [[maps1, liste_perso1, screen1],[maps2, liste_perso2, screen2],...]
    fps = pygame.time.Clock()  # mise en place d'une horloge
    liste_screen = []  # liste des fenetres à l'écran
    for i in arg:
        print_perso(i[0], i[2], i[1])  # on affiche tout les terrains dans un premier temps
        liste_screen.append(i[2])  # on remplie une liste avec les differentes fenetres
    while True:
        fps.tick(50)  # limitation des fps de la page
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        while test_keyboard("left ctrl"):  # deplacement de la fenetre en appuyant sur left ctrl
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if pygame.mouse.get_pressed()[0] == 1:
                x1, y1 = pygame.mouse.get_pos()
                deplace_screen(liste_screen, x1, y1)
        else:  # jeu normal
            x1, y1 = pygame.mouse.get_pos()
            screen_on = what_screen(x1, y1, liste_screen)  # on trouve l'écran utilisé
            num_arg = liste_screen.index(screen_on)
            maps, liste_perso, screen_on = arg[num_arg]  # les personnages, écran et terrain associé à l'écran
            game(maps, liste_perso, screen_on, False)  # on lance la fonction de jeu standart sans boucle