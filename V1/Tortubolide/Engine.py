import turtle

from Tortubolide.Tortubolide import Tortubolide
from Tortubolide.Bots import *

from Tortubolide.Vecteur import Vecteur


class Jeu:
    def __init__(self, map_path):

        self.screen = turtle.Screen()
        self.screen.tracer(0)
        self.taille_case = 20

        self.grille = []
        with open(map_path, 'r') as f:
            for ligne in f: self.grille.append(list(ligne.strip('\n')))
        
        self.hauteur = len(self.grille)
        self.largeur = max(len(row) for row in self.grille)
        self.dessiner_circuit()
        
        self.fantome = turtle.Turtle()
        self.fantome.hideturtle()
        self.fantome.penup()
        
        start_pos = self.trouver_depart()
        self.participants = [
            Tortubolide(start_pos, self.creer_tortue("green"), self, "Joueur 1", is_bot=False),
            #Tortubolide(start_pos, self.creer_tortue("red"), self, "Joueur 2", is_bot=False),
            Tortubolide(start_pos, self.creer_tortue("orange"), self, "Robot Prudent", is_bot=True, comportement=comportement_prudent),
            Tortubolide(start_pos, self.creer_tortue("blue"), self, "Robot Fou", is_bot=True, comportement=comportement_full_send)
        ]
        
        self.index_courant = 0
        self.setup_controles()
        self.actualiser_cycle()


    def creer_tortue(self, couleur):
        t = turtle.Turtle()
        t.shape("turtle")
        t.color(couleur)
        return t


    def actualiser_cycle(self):
        p = self.participants[self.index_courant]
        
        if p.tours >= 3:
            print(f"FIN : {p.nom} a gagné !")
            self.screen.textinput("Gagné !", f"{p.nom} l'emporte !")
            self.screen.bye()
            return

        if p.is_bot:
            
            acc = p.comportement(p)
            self.screen.ontimer(lambda: self.executer_tour(acc), 400)
        else:
            self.afficher_projections(p)


    def executer_tour(self, acc: Vecteur):
        p = self.participants[self.index_courant]
        p.action(acc)
        self.index_courant = (self.index_courant + 1) % len(self.participants)
        self.screen.update()
        self.actualiser_cycle()


    def afficher_projections(self, p):
        self.screen.tracer(0)
        self.fantome.clear()

        touches = {'z':Vecteur(0,-1), 'x':Vecteur(0,1), 'q':Vecteur(-1,0), 'd':Vecteur(1,0), 's':Vecteur(0,0)}

        for k, acc in touches.items():

            dest, col = p.simuler_deplacement(p.speed, acc)

            self.fantome.goto(self.convert_coords(dest))
            self.fantome.dot(8, "red" if col else "royalblue")
            self.fantome.write(f" {k}", font=("Arial", 8, "bold"))

        self.screen.update()
        self.screen.tracer(1)


    def trouver_depart(self):

        for y, ligne in enumerate(self.grille):
            for x, case in enumerate(ligne):
                if case == '0': return Vecteur(x, y)

        return Vecteur(1, 1)


    def convert_coords(self, v):
        return ((v.x - self.largeur/2)*self.taille_case, (self.hauteur/2 - v.y)*self.taille_case)


    def get_case(self, v):
        if 0 <= v.y < self.hauteur and 0 <= v.x < len(self.grille[int(v.y)]):
            return self.grille[int(v.y)][int(v.x)]
        return '#'


    def est_mur(self, v): return self.get_case(v) == '#'


    def dessiner_circuit(self):
        c = turtle.Turtle(); c.penup(); c.hideturtle()

        for y, ligne in enumerate(self.grille):
            for x, case in enumerate(ligne):
                if case in ('#', '0'):
                    c.goto(self.convert_coords(Vecteur(x,y)))
                    c.color("black" if case == '#' else "red")
                    c.dot(self.taille_case - 2)


    def setup_controles(self):

        self.screen.listen()

        self.screen.onkey(lambda: self.executer_tour(Vecteur(0,-1)) if not self.participants[self.index_courant].is_bot else (), "z")
        self.screen.onkey(lambda: self.executer_tour(Vecteur(0,1)) if not self.participants[self.index_courant].is_bot else (), "x")
        self.screen.onkey(lambda: self.executer_tour(Vecteur(-1,0)) if not self.participants[self.index_courant].is_bot else (), "q")
        self.screen.onkey(lambda: self.executer_tour(Vecteur(1,0)) if not self.participants[self.index_courant].is_bot else (), "d")
        self.screen.onkey(lambda: self.executer_tour(Vecteur(0,0)) if not self.participants[self.index_courant].is_bot else (), "s")