import random
from Tortubolide.Vecteur import Vecteur


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