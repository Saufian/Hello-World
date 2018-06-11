  # -*- coding: utf-8 -*-

from map_generator import*

Screen.main = pygame.display.set_mode()
# pygame.display.toggle_fullscreen()
Screen.source = "paramScreen.txt"
test = Screen(1000, 400, (300, 300), 0, "Test")  # initialisation de GuerreEtCivilisation (resolution de l'affichage)
main = Screen(0, 0, (1300, 700), -1, "Base")
print(Screen.main.get_rect())
font = Screen(0, 0, Screen.main.get_rect()[2:], -1)

load_pygame_skin("Data/listeSkinLand.txt")  # recuperation des skins dans le fichier dans data

toto = Perso("moi")  # creation d'un personnage
toto.set_graphism(pygame.image.load("Data/Perso1_face1.png"))  # mise en place du skin
toto.set_coord(6, 7)  # positionnement

titi = Perso("perso 2")  # creation d'un second personnage
titi.set_graphism(pygame.image.load("Data/Perso2_face1.png"))
titi.set_coord(3, 3)  # placement aux coordonnees (3, 3)

tata = Perso("perso 3")  # creation d'un troisieme perso
tata.set_graphism(pygame.image.load("Data/Perso3_face1.png"))
tata.set_coord(3, 5)  # placement en position (3, 5)

listePerso = [toto, titi, tata]  # liste contenant les persos
print("listePerso contient les personnages")


petit_ile = Maps()  # une nouvelle map pour faire les tests
petit_ile.load_map("Data/ile.txt")  # creation d'une map "ile" (taille:11/11 ; type "ile")
# tata.print_perso(a, font)  # affichage du perso sur la map1 aux coordonnées de celui ci

print  # un retour a la ligne pour la lisibilité
# toto.test_move(a)  # test d'affichage des mouvements

print_perso(petit_ile, main, listePerso)  # affichage des perso de la liste 'listePerso'

grand_ile = Maps()  # creation de la map de grande taille
grand_ile.load_map("Data/Map1Ile.txt")

vide = Maps(1, 1)

game_window([[petit_ile, [tata], main], [grand_ile, [toto, titi], test], [vide, [], font]])