import turtle
from Tortubolide.Vecteur import Vecteur


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