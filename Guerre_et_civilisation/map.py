# -*- coding: utf-8 -*-

import pygame
import gec_motor as motor


class Land:  # objet Land, qui compose les cartes de jeu.
    def __init__(self, ref):
        # création de map, avec un type pour l'identification et pour l'affichage si pas de graphisme spéciaux définis
        self.state = ref
        self.graphism = None  # pas de graphisme par défaut
        self.hauteur = 0  # correspond a la hauteur de l'élément. Un personnage basique ne peut pas monter 1 de hauteur
        self.spe = []  # ajoute des caractéristiques spéciales
        self.name = None

    def set_state(self, ref):  # changement du type de terrain
        self.state = ref

    def set_spe(self, typ):  # met en place les caractéristiques spéciales
        if not (typ in self.spe):  # vérification de la non présence (pas de doublon)
            self.spe.append(typ)

    def get_spe(self, typ):  # renvoi "True" si le terrain a la caractéristique spéciale typ
        return typ in self.spe

    def set_name(self, ref):  # possibilité de donner un nom au terrain
        self.name = ref

    def set_hauteur(self, nb):
        self.hauteur = nb
        self.upgrade_graphism()  # mise à jour des graphismes

    def set_graphism(self, graph):  # changement des graphisme pour ce terrain
        self.graphism = graph

    # TODO  ameliorer le code ci-dessous
    def get_graphism(self):
        # renvoi les graphismes pour l'affichage de l'objet : la valeur associé au type de terrain ( par defaut )
        # ou une apparence bien spécifique sous la forme de Str
        if self.graphism is not None:  # si les graphismes ont déjà été initialisé
            return self.graphism
        else:
            self.graphism = self.upgrade_graphism()  # sinon définir les paramètres
            return self.graphism

    def upgrade_graphism(self):
        skin_final = pygame.Surface((32, 32))  # taille d'une image du terrain (correspond a la resolution d'une case)
        for i in LoadSkin.listeLoad:  # récupération des différents graphismes
            if self.state == i.ref:  # si le nom de l’état du terrain correspond avec le nom du skin
                skin_final.blit(i.pygameImage, (0, 0))  # récupérer la surface (de pygame) correspondante
                # return self.graphism# retourner les bons graphismes
                for j in LoadSkin.listeLoad:  # vérification que les graphismes pour représenter la hauteur sont définis
                    if "denivele" == j.ref:
                        for loop in range(int(self.hauteur)):
                            # on fait apparaitre {hauteur} fois les graphismes pour montrer le dénivelé
                            skin_final.blit(j.pygameImage, (0, 32 - ((self.hauteur + 1) * 8)))
                            # positionnement du rajout
                return skin_final
        return "ERROR"


class Maps:
    lastMapPrint = [[], []]

    def __init__(self, xmax=0, ymax=0, typ="vide"):
        # création d'une map de taille "xmax","ymax",stocké dans la liste "name", rempli de Land de type "typ"
        self.contenu = []
        for x in range(xmax):
            self.contenu.append([])
            for y in range(ymax):
                self.contenu[x].append(Land(typ))

    def create_map(self, xmax, ymax, typ="vide"):
        # création d'une map de taille "xmax","ymax", stocké dans la liste "name", rempli de Land de type "typ"
        del self.contenu[:]
        for x in range(xmax):
            self.contenu.append([])
            for y in range(ymax):
                self.contenu[x].append(Land(typ))

    def print_map(self, screen, x=0, y=0, largeur=-1, hauteur=-1, refresh=True):
        if largeur == -1 or largeur > len(self.contenu):
            largeur = len(self.contenu)
        if hauteur == -1 or hauteur > len(self.contenu[0]):
            hauteur = len(self.contenu[0])
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x >= largeur:
            if x < 1:
                largeur += (x - largeur) + 1
            else:
                x -= (x - largeur) + 1
        if y >= hauteur:
            if y < 1:
                hauteur += (y - hauteur) + 1
            else:
                y -= (y - hauteur) + 1

        # TODO : mette en place un système de sauvegarde
        # qui utilise une mémoire des 10 derniers affichage(en cas de réutilisation)
        #
        # if [x,y,largeur,hauteur] in Maps.lastMapPrint[0]:
        # ecran=Maps.lastMapPrint[1][Maps.lastMapPrint[0].index([x,y,largeur,hauteur])]# (1180 , 630)
        # 	ecran=pygame.transform.scale(ecran,(1180,630))
        # 	screen.get_surface().blit(ecran,(0,0))
        # 	pygame.display.flip()
        # else:
        size_screen = screen.get_size()
        for i in range(y, hauteur):
            for j in range(x, largeur):
                skin = self.contenu[j][i].get_graphism()
                skin = pygame.transform.scale(skin, (size_screen[0] // (largeur - x),
                                                     size_screen[1] // (hauteur - y)))
                screen.surface.blit(skin, (j * (size_screen[0] // (largeur - x)),
                                           i * (size_screen[1] // (hauteur - y))))
        # last_map_use([x,y,largeur,hauteur],screen.surface)
        if refresh:
            motor.condense_screen()
            pygame.display.flip()
        else:
            return screen.surface, size_screen[0] // (largeur - x), size_screen[1] // (hauteur - y)

    def load_map(self, doc, complexite=1):  # complexite correspond au niveau de détail de la map
        data = charge_mot(doc, 1)  # data contient toutes les informations sur la map
        del self.contenu[:]  # on vide la map précédente pour être sur de ne pas réécrire dessus
        for x in range(len(data[0])):
            self.contenu.append([])
            for y in range(len(data)):
                self.contenu[x].append(Land(data[y][x]))  # on relie chaque info de data avec les objets adapté
        if complexite > 1:  # obligatoire de faire du cas par cas
            if complexite >= 2:  # détail sur l'altitude
                data = charge_mot(doc, 2)
                for x in range(len(data[0])):
                    for y in range(len(data)):
                        self.contenu[y][x].set_hauteur(float(data[x][y]))
                        # attention a l'ordre du contenu dans les coordonnées

    def refresh(self):
        for i in range(len(self.contenu)):
            for j in range(len(self.contenu[i])):
                self.contenu[i][j].set_graphism(None)


def last_map_use(data, screen):
    # fonction non finalisé, doit pouvoir mettre en mémoire les informations des dernières map affichées
    # pour accélérer le processus
    Maps.lastMapPrint[0].append(data)
    Maps.lastMapPrint[1].append(screen.surface)
    while len(Maps.lastMapPrint[0]) > 10:
        for i in range(1, len(Maps.lastMapPrint[0])):
            Maps.lastMapPrint[0][i - 1] = Maps.lastMapPrint[0][i]
            Maps.lastMapPrint[1][i - 1] = Maps.lastMapPrint[1][i]
        del (Maps.lastMapPrint[0][len(Maps.lastMapPrint[0]) - 1])
        del (Maps.lastMapPrint[1][len(Maps.lastMapPrint[1]) - 1])


def charge_mot(doc, complexite=1):
    # fonction d'extraction de données dans un DOCument
    # jusqu'à trouver une ligne avec seulement le mot "fin" [complexite] fois
    save_file = open(doc, 'r')  # on ouvre le doc en mode lecture
    retour = []
    for i in range(complexite):
        retour = []  # on ne capte ainsi que le contenu du [complexite] bloc finissant par "fin"
        line = save_file.readline()  # attention, le retour a la ligne est aussi récupéré
        line = line[:len(line) - 1]  # on supprime le retour a la ligne.
        while line != "fin":  # on prend toutes les lignes jusqu'à trouver le mot "fin"
            retour.append(line.split(" ")[:])  # on sépare chaque mot de la ligne
            line = save_file.readline()  # on prend la ligne suivante
            line = line[:len(line) - 1]  # on supprime le retour a la ligne de la nouvelle ligne
    save_file.close()  # on oublie pas de fermer le doc
    return retour


def load_pygame_skin(doc):
    # fonction principale dans le chargement des images
    # --> va charger toutes les images dont les adresses sont contenus dans le DOCument.
    # le document doit être de la forme : [nom du skin] [adresse du skin]
    data = charge_mot(doc)
    for i in data:  # pour chaque skin, créer un objet de LoadSkin
        load = LoadSkin(i[0])  # associe le nom
        if len(i) == 2:  # pas de troisième entrée
            load.set_skin(i[1])


class LoadSkin:
    listeLoad = []  # contient les objets avec les skins

    def __init__(self, ref, frame=0):
        self.ref = ref  # nom du skin
        self.frame = frame  # inutilisé pour l'instant
        self.pygameSkinLocation = None  # contiendra l'adresse du skin
        self.pygameImage = None  # contiendra directement la surface associé à l'adresse
        # (pas nescessaire dans tous les cas)
        LoadSkin.listeLoad.append(self)  # ajoute chaque objet à la liste

    def set_skin(self, pygame_skin_location):  # met en place les graphismes de cet objet
        self.pygameSkinLocation = pygame_skin_location  # adresse
        self.pygameImage = pygame.image.load(pygame_skin_location)  # surface associée