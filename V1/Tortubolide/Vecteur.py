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