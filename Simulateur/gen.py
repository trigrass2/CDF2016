#!/usr/bin/python3.4

import random
import copy


class Data:
    def __init__(self):
        self.taux_select = 0.4  # proportion des individus selectionnes dans la population finale
        self.taux_croisements = 0.4  # proporttion des individus issus de croisements dans la population finale

        self.taux_mutation = 0.1  # pourcentage de flou dans la mutation

        self.nb_croisements = 2


def eval_pop(pop):
    '''
	pop : liste de listes de poids
	'''


# appel du simulateur

def select_pop(pop, scores, data):
    '''
	pop : liste de listes de poids
	scores : listes de scores obtenus par chacun des individus (lors de l'evaluation)

	renvoit une nouvelle population
	'''

    new_pop = []
    len_reseau = len(pop[0])

    # tri de la population par score decroissant
    taille = len(scores)
    index = [(scores[i], i) for i in range(taille)]

    index.sort(reverse=True)
    index = [index[i][1] for i in range(taille)]

    # creation de la roulette
    total_score = sum(scores)
    roulette = []

    for i in index:
        rate = int(round((scores[i] / total_score) * 360))
        roulette += [i] * rate

    # selection des elements de base de la nouvelle population
    nb_tours = int(round(data.taux_select * taille))

    for i in range(nb_tours):
        rd = random.randint(0, 359)
        new_pop.append(copy.deepcopy(pop[roulette[rd]]))

    taille -= nb_tours
    nlen = nb_tours

    # on croise les individus selectionnes pour reconstituer une autre partie de notre population
    nb_tours = int(round(data.taux_croisements * taille))
    taille_gene = len_reseau // data.nb_croisements

    for i in range(nb_tours):
        indiv = []

        for j in range(data.nb_croisements):
            rd = random.randint(0, nlen - 1)

            if j == data.nb_croisements - 1:
                indiv += new_pop[rd][j * taille_gene:]
            else:
                indiv += new_pop[rd][j * taille_gene:(j + 1) * taille_gene]

        new_pop.append(copy.deepcopy(indiv))

    taille -= nb_tours
    nlen += nb_tours

    # on effectue ensuite des mutations sur des individus selectionnes au hasard dans notre population
    for i in range(taille):
        rd1, rd2 = random.randint(0, nlen - 1), random.randint(0, nlen - 1)
        rd3, rd4 = random.randint(0, len_reseau - 1), random.randint(0, len_reseau - 1)

        indiv = copy.deepcopy(new_pop[rd1])

        indiv[rd3] = new_pop[rd2][rd4]  # on remplace un gene par une valeur probable

        indiv[rd3] = indiv[rd3] + random.uniform(-data.taux_mutation, data.taux_mutation) * indiv[
            rd3]  # et on la modifie legerement

        new_pop.append(copy.deepcopy(indiv))

    return (new_pop)


def main():
    data = Data()
    select_pop([[1212, 35, 15, 32, 12], [15, 125, 12, 324, 45], [1221, 12, 35, 75, 566], [30, 124, 1212, 35, 56],
                [45, 656, 1222, 14, 15], [124, 535, 10, 1, 12]], [20, 1, 5, 15, 25, 12], data)


if __name__ == '__main__':
    main()
