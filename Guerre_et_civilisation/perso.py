# -*- coding: utf-8 -*-
import copy  # pour pouvoir travailler sur des maps avec les perso sans modifier les maps originales.
from map import *
import gec_motor as motor


class Perso:  # permet de créer des objets personnages(en mouvement sur la map)
    def __init__(self, ref, stat=None):  # un identifiant, et une liste de stats de la forme [[a],[x]]
        if stat is None:  # (si non donné en argument : réalisé mais vide)
            stat = [[], []]
        self.ref = ref
        self.stat = stat
        self.graphism = None
        self.oldGraphism = None  # graphisme réservé pour l'affichage sur le terminal pour le debuggage
        self.coord = [0, 0]
        self.spe = []  # création de caractéristiques spéciales (de type booléen (ex: nage ou nage pas))
        self.travel = [["vide", "lave", "plaine", "montagne", "eau", "foret", "spawn", "objectif"],
                       [-1, -1, 0, 3, 3, 2, 0, 1]]  # difficulté a traverser une case de terrain donné
        # (de la forme [[type terrain],[dif]] (liste non exhaustive)

    def set_coord(self, x, y):  # mise en place et modifications des coordonnées du personnage sur les maps
        self.coord[0] = x
        self.coord[1] = y

    def dif_travel(self, typ, nb):
        # calcul de la difficulté d'un voyage (type du terrain, déplacement sans la difficulté)
        if typ in self.travel[0]:  # si le terrain est répertorié
            position = self.travel[0].index(typ)  # position de la donnée relative à ce terrain dans la liste
            dif = self.travel[1][position]  # difficulté associer à ce terrain
            return nb + dif  # retourne l'éloignement plus la difficulté de traverser
        else:
            print("Land type unknow : " + str(typ))  # affiche un message d'erreur si le terrain est inconnu
            return -1  # rend le terrain impraticable

    def add_spe(self, special):  # permet d'ajouter une capacité spéciale
        self.spe.append(special)

    def del_spe(self, special):  # permet de retirer une capacité spéciale
        if special in self.spe:  # si la capacité spéciale est présente
            del self.spe[self.spe.index(special)]  # suppression de la capacité spéciale
        else:
            print("this special doesn't exist")  # sinon, affichage d'un message d'erreur

    def get_spe(self, special):  # retourne la possession ou non de la capacité "special"
        return special in self.spe

    def set_graphism(self, graph):  # mise en place de l'affichage du personnages (skin)
        self.graphism = graph

    def get_graphism(self):  # renvoi le skin du personnage
        if self.graphism is not None:
            return self.graphism
        else:
            print("no skin")
            return self.ref

    def add_stat(self, name_stat, nb):  # ajout de Statistique au personnage (nom de la nouvelle stat, valeur initial)
        if name_stat in self.stat[0]:
            self.change_stat(name_stat, nb)
            print("Stat already create")
        else:
            self.stat[0].append(name_stat)
            self.stat[1].append(nb)

    def change_stat(self, name_stat, nb):
        # changement de valeur d'une stat déjà possédé (nom de la stat, nouvelle valeur)
        if name_stat in self.stat[0]:  # test pour savoir si la statistique existe avant de la changer.
            position = self.stat[0].index(name_stat)
            self.stat[1][position] = nb
        else:
            print("no stat")  # sinon, message d'erreur

    def get_stat(self, name_stat):  # retourne l’état de la stat "name_stat"
        if name_stat in self.stat[0]:  # si c'est une stat qui est dans la liste
            position = self.stat[0].index(name_stat)  # trouve la position de la stat
            return self.stat[1][position]  # retourne la valeur associé
        else:
            print("no stat")  # sinon ->message d'erreur

    def del_stat(self, name_stat):
        if name_stat in self.stat[0]:  # si c'est une stat qui est dans la liste
            position = self.stat[0].index(name_stat)  # trouve la position de la stat
            del self.stat[0][position]
            del self.stat[1][position]  # retourne la valeur associé
        else:
            print("no stat")  # sinon ->message d'erreur

    def print_perso(self, map_use, screen):
        # affichage de la carte+le perso ( sur un ecran de taille screenWidth, screenHeight
        # donné par screen.get_size()[0] et screen.get_size()[1])
        position = self.coord  # récupération de la position des perso
        data_map = map_use.print_map(screen, refresh=False)
        screen.set_surface(data_map[0])  # mise en mémoire des graphismes de la map dans l'écran associé
        taillex = data_map[1]
        tailley = data_map[2]
        if 0 <= position[0] < len(map_use.contenu) and 0 <= position[1] < len(map_use.contenu[0]):
            # sécurité pour éviter les dépassement hors tableau
            skin = pygame.transform.scale(self.get_graphism(), (taillex, tailley))
            # work[position[0]][position[1]]=self  # remplacement du de l'objet dans le tableau
            # (on peut y faire en meme temps pour d'autres Perso)
            screen.surface.blit(skin, (position[0] * taillex, position[1] * tailley))

            # remplacement de l'objet dans le tableau (on peut y faire en même temps pour d'autres Perso)
        motor.condense_screen()
        pygame.display.flip()

    def test_move(self, maps, liste_perso=None):
        # affiche la map avec la valeur nécessaire au déplacement (avec la liste des position déjà prise)
        if liste_perso is None:  # si aucune liste n'est donné, on en réalise une vide
            liste_perso = []
        if len(liste_perso) == 0:  # si la liste est vide
            liste_perso.append(self)  # mettre le personnage "self" dedans
        save = copy.deepcopy(maps.contenu)  # on crée une sauvegarde indépendante de la carte de base
        liste = []  # création de la liste dans laquelle on ira stocker les différentes valeurs de déplacement
        # triées en fonction de la difficulté
        work = clone_list(save)  # work devient une copie de save
        maxi = len(save) * len(save[0]) + 1  # on ajoute 1 pour être sur que cette valeur soit indépassable
        for i in range(maxi):  # création de la liste de coordonnées des différentes valeurs (de 0 à maxi)
            liste.append([i, [], []])
            # liste des valeurs de la forme:[dif,[liste des abscisses des cases ayant cette difficulté],[ordonnée]]
        for i in range(len(save)):
            for j in range(len(save[0])):  # on regarde les cases une par une pour leur donner une valeur de départ
                typ = save[i][j].state
                if typ == "vide" or typ == "eau" or typ == "lave":
                    # liste non exhaustive des cases que l'on ne peut pas franchir
                    # TODO : regarder en fonction des capacité du personnage
                    work[i][j].set_graphism(-10)
                    # mettre une valeur négative sur les cases infranchissable (on met la valeur sur les graphisme)
                else:
                    work[i][j].set_graphism(maxi)
                    # les cases normales ont une valeur maximales, que l'ont fera baisser le plus possible
        for i in liste_perso:  # pour chaque personnage
            temp_coord = i.coord
            work[temp_coord[0]][temp_coord[1]].set_graphism(-10)  # rajouter les positions prises des autres personnages
        liste[0][1].append(self.coord[0])
        liste[0][2].append(self.coord[1])  # on ajoute la position du 0 a la liste (de la forme [nb,[x1,xn],[y1,yn]])
        nb = 0
        # mise a 0 du curseur qui indiquera l'avancement dans ce travail (et le numéro des cases que l'on va modifier)
        for j in range(maxi):
            # on refait l’opération jusqu’à ce que cela soit impossible d'avoir une case avec un nombre plus grand
            for i in range(len(liste[nb][1])):  # nombre de case a une distance nb du perso
                x = liste[nb][1][i]
                y = liste[nb][2][i]
                if (x + 1) < len(save[0]):  # test successif pour éviter les dépassements de variables
                    dif = self.dif_travel(save[x + 1][y].state, nb + 1)
                    if save[x + 1][y].get_graphism() > dif and \
                            (-1 <= save[x][y].hauteur - save[x + 1][y].hauteur - save[x][y].hauteur <= 1):
                        # on test voir si la case a une valeur supérieure à celle possible
                        # en faisant une simulation, en récupérant les coordonnées de la case,
                        # la valeur actuelle (dans les graphismes), et en comparant avec la valeur voulue
                        # (obtenu avec "dif", qui récupère le type de terrain, la difficulté normale
                        # (sans les caractéristiques du terrain), et les rassemble avec la difficulté propre
                        # au personnage). Puis on regarde si la hauteur n'est pas trop importante
                        # (entre -1 et 1 de dif ----->>>>inclu)
                        work[x + 1][y].set_graphism(dif)  # en dessous de work
                        # on note les coordonnées des cases pour pouvoir revenir dessus à la prochaine boucle
                        liste[dif][1].append(x + 1)
                        liste[dif][2].append(y)
                        # on recommence avec la case suivante située proche
                if (x - 1) >= 0:  # test successif pour éviter les dépassements de variables
                    dif = self.dif_travel(save[x - 1][y].state, nb + 1)
                    if save[x - 1][y].get_graphism() > dif and \
                            (-1 <= save[x][y].hauteur - save[x - 1][y].hauteur - save[x][y].hauteur <= 1):
                        work[x - 1][y].set_graphism(dif)  # au dessus de work
                        liste[dif][1].append(x - 1)
                        liste[dif][2].append(y)
                        # on recommence avec la case suivante situé proche
                if (y - 1) >= 0:  # test successif pour éviter les dépassements de variables
                    dif = self.dif_travel(save[x][y - 1].state, nb + 1)
                    if save[x][y - 1].get_graphism() > dif and \
                            (-1 <= save[x][y].hauteur - save[x][y - 1].hauteur - save[x][y].hauteur <= 1):
                        work[x][y - 1].set_graphism(dif)  # a gauche de work
                        liste[dif][1].append(x)
                        liste[dif][2].append(y - 1)
                        # on recommence avec la case suivante situé proche
                if (y + 1) < len(save):  # test successif pour éviter les dépassements de variables
                    dif = self.dif_travel(save[x][y + 1].state, nb + 1)
                    if save[x][y + 1].get_graphism() > dif and \
                            (-1 <= save[x][y].hauteur - save[x][y + 1].hauteur - save[x][y].hauteur <= 1):
                        work[x][y + 1].set_graphism(dif)  # a droite de work
                        liste[dif][1].append(x)
                        liste[dif][2].append(y + 1)
            nb += 1  # on passe a la valeur suivante
        work[self.coord[0]][self.coord[1]].set_graphism(0)  # remise à 0 de la positon du personnage
        for i in range(len(save)):  # pour chaque case du terrain
            for j in range(len(save[0])):
                if work[i][j].get_graphism() < 0:  # si la valeur est négative, alors ce sont des terrains inaccessible
                    work[i][j].set_graphism(maxi)  # on leurs met la valeur max
        return work, maxi

    def range_travel(self, map_use, distance, screen, liste_perso=None):
        if liste_perso is None:  # si aucune liste n'est donné, on en réalise une vide
            liste_perso = []
        view = Maps()
        view.contenu = copy.deepcopy(map_use.contenu)
        work = self.test_move(map_use, liste_perso)[0]
        for i in range(len(view.contenu)):  # pour chaque case du terrain
            for j in range(len(view.contenu[0])):
                if work[i][j].get_graphism() <= distance:
                    view.contenu[i][j].set_graphism(work[i][j].get_graphism())
        if len(liste_perso) == 0:
            self.print_perso(view, screen)
        else:
            if not (self in liste_perso):
                liste_perso.append(self)
            print_perso(view, screen, liste_perso)

    def chemin(self, map_use, x, y, liste_perso=None):
        if liste_perso is None:  # si aucune liste n'est donné, on en réalise une vide
            liste_perso = []
        result = self.test_move(map_use, liste_perso)
        move = result[0]
        maxi = result[1]
        if x < 0:
            x = 0
        elif x > len(move):
            x = len(move)-1
        if y < 0:
            y = 0
        elif y > len(move[0]):
            y = len(move[0])-1
        if move[x][y].get_graphism() < maxi:
            liste = [[x, y]]
            compt = maxi  # le compt est une sécurité pour ne pas boucler à l'infinie
            while move[x][y].get_graphism() > 1 and compt > 0:
                if move[x + 1][y].get_graphism() < move[x][y].get_graphism():
                    x += 1
                elif move[x - 1][y].get_graphism() < move[x][y].get_graphism():
                    x -= 1
                elif move[x][y + 1].get_graphism() < move[x][y].get_graphism():
                    y += 1
                elif move[x][y - 1].get_graphism() < move[x][y].get_graphism():
                    y -= 1
                liste.append([x, y])
                compt -= 1
            return liste
        else:
            print("pas de chemin")
            return None

    def move(self, map_use, screen, x, y, liste_perso=None):
        if liste_perso is None:  # si aucune liste n'est donné, on en réalise une vide
            liste_perso = []
        liste = self.chemin(map_use, x, y, liste_perso)
        if liste is not None:
            self.print_perso(map_use, screen)
            for i in range(len(liste)):
                self.set_coord(liste[len(liste) - i - 1][0], liste[len(liste) - i - 1][1])
                if len(liste_perso) == 0:
                    self.print_perso(map_use, screen)
                else:
                    if not (self in liste_perso):
                        liste_perso.append(self)
                    print_perso(map_use, screen, liste_perso)
        else:
            print("pas de mouvement")


def print_perso(map_use, screen, liste_perso):
    data = map_use.print_map(screen, refresh=False)
    screen.surface.blit(data[0], data[0].get_rect())
    for i in liste_perso:
        position = i.coord  # recuperation de la position des perso
        if 0 <= position[0] < len(map_use.contenu) and 0 <= position[1] < len(map_use.contenu[0]):
            # pour éviter les dépassement hors tableau
            screen.surface.blit(pygame.transform.scale(i.get_graphism(), (data[1], data[2])),
                                (position[0] * data[1], position[1] * data[2]))
            # remplacement de l'objet dans le tableau
    motor.condense_screen()
    pygame.display.flip()


def clone_list(liste):
    # retourne une liste qui est une copie de celle en entrée avec une mutabilité étrange (utilisé dans test_move())
    clone = []
    for i in range(len(liste[0])):
        clone.append((liste[i])[:])
    return clone