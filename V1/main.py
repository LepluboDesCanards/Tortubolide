import turtle
import random

class Vecteur:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vecteur(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vecteur(self.x - other.x, self.y - other.y)
    
    def __iter__(self):
        return iter((self.x, self.y))


class Tortubolide:
    def __init__(self, pos: Vecteur, body: turtle.Turtle, jeu, nom="Joueur", is_bot=False, comportement=None):
        
        self.pos = pos
        self.body = body
        self.jeu = jeu
        self.nom = nom
        self.is_bot = is_bot
        self.comportement = comportement # Une fonction qui prend 'self' en argument
        
        self.speed = Vecteur(0, 0)
        self.tours = 0
        self.sur_ligne_depart = True
        
        self.body.speed(0)
        self.body.penup()
        self.body.goto(self.jeu.convert_coords(self.pos))
        self.body.pendown()
        self.body.stamp()


    def simuler_deplacement(self, v_actuelle, acceleration):
        v_test = v_actuelle + acceleration
        derniere_pos = self.pos
        

        pas_x = 1 if v_test.x > 0 else -1 if v_test.x < 0 else 0
        pas_y = 1 if v_test.y > 0 else -1 if v_test.y < 0 else 0
        nb_etapes = max(abs(v_test.x), abs(v_test.y))
        

        for i in range(1, nb_etapes + 1):
            ix = self.pos.x + (i * pas_x if i <= abs(v_test.x) else v_test.x)
            iy = self.pos.y + (i * pas_y if i <= abs(v_test.y) else v_test.y)

            test_pos = Vecteur(int(ix), int(iy))

            if self.jeu.est_mur(test_pos):
                return derniere_pos, True
            
            derniere_pos = test_pos

        return derniere_pos, False


    def action(self, acc: Vecteur):
        
        self.body.clearstamps(1)
        self.body.stamp()
        
       
        nouvelle_pos, collision = self.simuler_deplacement(self.speed, acc)
        
        if collision:
            self.pos = nouvelle_pos
            self.speed = Vecteur(0, 0)

        else:
            self.speed += acc
            self.pos = nouvelle_pos
            
            
            if self.jeu.get_case(self.pos) == '0':
                if not self.sur_ligne_depart:
                    self.tours += 1
                    self.sur_ligne_depart = True
                    print(f"[{self.nom}] Passage ligne ! Tours : {self.tours}/3")
            else:
                self.sur_ligne_depart = False
            
        self.body.goto(self.jeu.convert_coords(self.pos))


def comportement_full_send(bot):
    return Vecteur(random.randint(-1, 1), random.randint(-1, 1))


def comportement_prudent(bot):

    possibilites = [Vecteur(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
    random.shuffle(possibilites)

    for acc in possibilites:
        _, collision = bot.simuler_deplacement(bot.speed, acc)
        if not collision:
            return acc
    return Vecteur(0, 0)


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

if __name__ == "__main__":
    jeu = Jeu("./V1/maps/dev.tmap")
    jeu.screen.mainloop()