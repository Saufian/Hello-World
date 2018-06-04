# -*- coding: utf-8 -*-
import sys
import pygame
from random import randint
import matplotlib.pyplot as plt

pygame.init()

size = width, height = 641, 641
tailleCase = 20
screen = pygame.display.set_mode(size)

# color=[(124, 16, 240), (122, 24, 232), (120, 32, 224), (118, 40, 216), (116, 48, 208), (114, 56, 200), (112, 64, 192),
# (110, 72, 184), (108, 80, 176), (106, 88, 168), (104, 96, 160), (102, 104, 152), (100, 112, 144), (98, 120, 136),
#  (96, 128, 128), (94, 136, 120), (92, 144, 112), (90, 152, 104), (88, 160, 96), (86, 168, 88), (84, 176, 80),
#  (82, 184, 72), (80, 192, 64), (78, 200, 56), (76, 208, 48), (74, 216, 40), (72, 224, 32), (70, 232, 24),
#  (68, 240, 16), (66, 248, 8), (8, 248, 32), (16, 240, 32), (24, 232, 32), (32, 224, 32), (40, 216, 32), (48, 208, 32),
#  (56, 200, 32), (64, 192, 32), (72, 184, 32), (80, 176, 32), (88, 168, 32), (96, 160, 32), (104, 152, 32),
#  (112, 144, 32), (120, 136, 32), (128, 128, 32), (136, 120, 32), (144, 112, 32), (152, 104, 32), (160, 96, 32),
#  (168, 88, 32), (176, 80, 32), (184, 72, 32), (192, 64, 32), (200, 56, 32), (208, 48, 32), (216, 40, 32),
#  (224, 32, 32), (232, 24, 32), (240, 16, 32), (248, 8, 32)]
color = [(124, 16, 240), (122, 24, 232), (120, 32, 224), (118, 40, 216), (116, 48, 208), (114, 56, 200), (112, 64, 192),
         (110, 72, 184), (108, 80, 176), (106, 88, 168), (104, 96, 160), (102, 104, 152), (100, 112, 144),
         (98, 120, 136), (96, 128, 128), (94, 136, 120), (92, 144, 112), (90, 152, 104), (88, 160, 96), (86, 168, 88),
         (84, 176, 80), (82, 184, 72), (80, 192, 64), (78, 200, 56), (76, 208, 48), (74, 216, 40), (72, 224, 32),
         (70, 232, 24), (68, 240, 16), (66, 248, 8), (8, 248, 32), (16, 240, 32), (24, 232, 32), (32, 224, 32),
         (40, 216, 32), (48, 208, 32), (56, 200, 32), (64, 192, 32), (72, 184, 32), (80, 176, 32), (88, 168, 32),
         (96, 160, 32), (104, 152, 32), (112, 144, 32), (120, 136, 32), (128, 128, 32), (136, 120, 32), (144, 112, 32),
         (152, 104, 32), (160, 96, 32), (168, 88, 32), (176, 80, 32), (184, 72, 32), (192, 64, 32), (200, 56, 32),
         (208, 48, 32), (216, 40, 32), (224, 32, 32), (232, 24, 32), (240, 16, 32), (248, 8, 32)]


class Unit:
    def __init__(self, data_niv=0, pos=(0, 0)):  # avec pos un tuple de la forme (posX,posY)
        self.niveau = data_niv  # niveau (d'entre -30 et 30 inclu)
        self.posX = pos[0]
        self.posY = pos[1]

    def set_niveau(self, niv):
        self.niveau = niv  # niveau (entre -30 et 30 inclu)

    def set_pos(self, x, y):
        self.posX = x
        self.posY = y

    def get_pos(self):
        return self.posX, self.posY

    def get_color(self):
        return color[self.niveau + 30]


def affiche(terrain):
    for x in range(width // tailleCase):
        for y in range(height // tailleCase):
            pygame.draw.rect(screen, terrain[x][y].get_color(),
                             (x * tailleCase, y * tailleCase, (x + 1) * tailleCase, (y + 1) * tailleCase))
                               # on fait des carres
    pygame.display.flip()


def pic(terrain, nb, mini, maxi, difa0, eloignement, liste_pic=None):
  # eloignement correspond au nombre de cases entre le point et les autres (fonctionne sous forme de carrés)
    if liste_pic is None:
        liste_pic = []
    if mini == 0:  # on change la valeur de base: on evite les 0 lors des divisions
        mini = 1
    if maxi == 0:
        maxi = -1

    if abs(mini) < difa0:  # on limite la taille des pics : on ne veux pas qu'ils soient plus petit que difa0
        mini = difa0 * (mini // abs(mini))
          # si le minimum de taille de pic est trop faible, on le met a la limite de difa0, en respectant son signe
    if abs(maxi) < difa0:  # meme chose avec le maximum
        maxi = difa0 * (maxi // abs(maxi))
    xmax = len(terrain) - 1  # on evite les depassements de variables
    ymax = len(terrain[0]) - 1
    compt = 0  # compteur de pics realise dans cet appel
    limite = nb * 10  # nombre maximum d'iteration, pour eviter la boucle infini
    comptcritique = 0  # compteur associé
    while compt < nb and comptcritique < limite:  # on s'arrete quand tout est créé, ou si on atteint le max d'iteration
        comptcritique += 1
        x = randint(0, xmax)  # position aleatoire
        y = randint(0, ymax)
        vide = True  # test sur la presence ou non de pics sur et autour de la position de
        for p in liste_pic:  # on test sur chaque pic deja existant
            if x - eloignement <= p.get_pos()[0] <= x + eloignement \
                    and y - eloignement <= p.get_pos()[1] <= y + eloignement and vide:  # si une position est deja prise
                vide = False
        if vide:  # si la place est libre, on crée un nouveau pic
            nouvniveau = 0
            comptcrit = 0
            while nouvniveau == 0:
                nouvniveau = randint(mini - (difa0 * (mini // abs(mini))), maxi - (difa0 * (maxi // abs(maxi))))
                  # on met un aleatoire qui va donner une valeur dans l'interval entre l'ecart et la limite
                  # (l'interval est plus petit, mais les signes sont respecté)
                comptcrit += 1
                if comptcrit == 50:  # 50 tentatives et que des 0 : on sort en donnant un résultat neutre
                    nouvniveau = 1
            nouvniveau += difa0 * (nouvniveau // abs(nouvniveau))
              # on rajoute la diference à 0, en faisant attention au signe
            terrain[x][y].set_niveau(nouvniveau)
            liste_pic.append(terrain[x][y])
            compt += 1  # un pic de plus, on ingremente le curseur
    if comptcritique == limite:
        print("maximum d'iteration atteint")  # averti du fait que l'on ai depassé le nombre limite
    return liste_pic


def descente(terrain, liste_pic, pente):  # avec la pente en pourcentage
    listefait = []  # contient les coordonnées (x,y) de la position des elements de terrain deja calculé
    if pente > 100:
        pente = 100
    compt = 0
    mesure = [[], []]
    listetrv = [temp.get_pos() for temp in liste_pic]
      # creation d'une liste contenant les positions des cases à travailler
    while len(listetrv) != 0:  # s'arrete quand la liste est vide
        for x in range(listetrv[-1][0] - 1, listetrv[-1][0] + 2):  # on prend les cases proches
            for y in range(listetrv[-1][1] - 1, listetrv[-1][1] + 2):
                if 0 <= x < len(terrain) and 0 <= y < len(terrain[0]) and not ((x, y) in listefait):
                  # on evite de sortir du terrain et de refaire des cas déjà fait
                    tauxdescente = terrain[listetrv[-1][0]][listetrv[-1][1]].niveau // (101 - pente)
                    if tauxdescente == 0:
                        tauxdescente = 1
                    if terrain[listetrv[-1][0]][listetrv[-1][1]].niveau < 0:  # cas où le pic est plus bas
                        if terrain[listetrv[-1][0]][listetrv[-1][1]].niveau < terrain[x][y].niveau:
                          # si le terrain proche doit etre abaissé (on ne fait pas monter des cases plus basse)
                            terrain[x][y].set_niveau(terrain[listetrv[-1][0]][listetrv[-1][1]].niveau
                                                     + randint(1, (-1 * tauxdescente)))
                                                       # on fait monter les zones proches
                            if not ((x, y) in listetrv):
                              # on pensera a regarder ce terrain, on evite les repetitions et ce qui est deja fait
                                listetrv.append(terrain[x][y].get_pos())
                    elif terrain[listetrv[-1][0]][listetrv[-1][1]].niveau > 0:
                      # cas dans lequel le terrain est plus haut que le sol
                        if terrain[listetrv[-1][0]][listetrv[-1][1]].niveau > terrain[x][y].niveau:
                            # si le terrain proche doit etre monté (on ne fait pas descendre des cases plus haute)
                            terrain[x][y].set_niveau(terrain[listetrv[-1][0]][listetrv[-1][1]].niveau
                                                     - randint(1, tauxdescente))
                                                       # on fait descendre les zones proches
                            if not ((x, y) in listetrv):
                              # on pensera a regarder ce terrain, on evite les repetitions et ce qui est deja fait
                                listetrv.append(terrain[x][y].get_pos())
        listefait.append(listetrv[-1])
        del listetrv[-1]
        print("listetrv = ", len(listetrv), "  listefait = ", len(listefait))
        if len(listefait) > 1 + compt:  # on peut régler ici le pas de l'affichage de la carte en temps réel
            compt = len(listefait)
            affiche(terrain)
        mesure[0].append(len(listetrv))
        mesure[1].append(len(listefait))
    plt.plot(mesure[1], mesure[0])
    plt.show()
    return listefait


# terrain=[[Unit(int((i+j)*(float(len(color))/float((width//tailleCase)+(height//tailleCase))))-30) for j in
# range(height//tailleCase)]for i in range (width//tailleCase)]

carte = [[Unit(0, (i, j)) for j in range(height // tailleCase)] for i in range(width // tailleCase)]
listePic = pic(carte, 4, -30, 30, 15, 15)
test = descente(carte, listePic, 0)

affiche(carte)

fps = pygame.time.Clock()  # mise en place d'une horloge
loop = True
while loop:
    fps.tick(10)  # limitation des fps de la page
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False