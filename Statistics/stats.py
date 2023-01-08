import os, sys

from Utils.constansts import WORLD_SIZE
from Utils.constansts import WORLD_SIZE_RANGE

class Statistiques:

    def __init__(self,
                 valeur_max=None,
                 valeur_min=None,
                 mediane=None,
                 moyenne=None,
                 liste_valeurs=[]):
        self.valeur_max = valeur_max
        self.valeur_min = valeur_min
        self.mediane = mediane
        self.moyenne = moyenne
        self.liste_valeurs = liste_valeurs

    def get_val_at_percentage(self, percentage=50):
        tmp = []
        if 0 <= percentage < 100:
            tmp = sorted(self.liste_valeurs)
            index = len(tmp)*(percentage/100)
            index = index - (index % 1)
            # print("index : " + str(index) + "\nlen(tmp) : " + str(len(tmp)))
            return tmp[int(index)]
        elif percentage == 100:
            tmp = sorted(self.liste_valeurs)
            try:
                return tmp[-1]
            except OverflowError:
                print("tmp len = " + str(len(tmp)))
                raise OverflowError
        else:
            print(percentage)
            raise Exception

    def __repr__(self):
        return "Statistiques :\n" + \
                "\tMax = " + str(self.valeur_max) + "\n" + \
                "\tMin = " + str(self.valeur_min) + "\n" + \
                "\tMed = " + str(self.mediane) + "\n" + \
                "\tMoy = " + str(self.moyenne) + "\n"

    def debug_percentages(self):
        for i in range(0, 110, 10):
            print(str(i) + " % : " + str(self.get_val_at_percentage(i)))


def perlin_stats(perlin):
    liste_valeurs = []
    for i in WORLD_SIZE_RANGE:
        for j in WORLD_SIZE_RANGE:
            liste_valeurs.append(float(perlin.get(i, j).value))

    # get(x, y)
    tmp = sorted(liste_valeurs)

    valeur_max = max(liste_valeurs)
    #print("max = " + str(valeur_max))
    valeur_min = min(liste_valeurs)
    #print("min = " + str(valeur_min))
    moyenne = sum(liste_valeurs) / len(liste_valeurs)

    if len(tmp) % 2 == 1:
        index = ((len(tmp)-1)/2)
        mediane = tmp[int(index)]
    else:
        index = (len(tmp)/2)-1
        mediane = (tmp[int(index)]+tmp[int(index+1)])/2

    stats = Statistiques(valeur_max, valeur_min,
                         mediane, moyenne, liste_valeurs)

    return stats



