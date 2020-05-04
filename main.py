import argparse
import api
import quoridor
from quoridorx import QuoridorX
import turtle


def analyser_commande():
    parser = argparse.ArgumentParser(description='Jeu Quoridor - phase 1')
    parser.add_argument('idul', metavar='idul', help='IDUL du joueur')
    parser.add_argument('-l', '--lister', dest='liste des parties', help='Lister les identifiants de vos 20 dernières parties.')

    parser.add_argument('idul', metavar='idul', dest='idul', help='IDUL du joueur')

    parser.add_argument('-a', '--automatique', metavar='idul', dest='automatique' , help='Jouer en mode automatique contre le serveur')

    parser.add_argument('-x', '--manuel', metavar='idul', dest='manuel', help='Jouer en mode manuel contre le serveur avec un affichage dans une fenêtre graphique')

    parser.add_argument('-ax', '--automatique_affich', metavar='idul', dest='automatique_affich', help='Jouer en mode automatique contre le serveur avec un affichage dans une fenêtre graphique')
    args= parser.parse_args()
    return args

def afficher_damier_ascii(état):
    titre = ''
    ligne2 = '   -----------------------------------'
    ligne3 = list('9 | .   .   .   .   .   .   .   .   . |')
    ligne4 = list('  |                                   |')
    ligne5 = list('8 | .   .   .   .   .   .   .   .   . |')
    ligne6 = list('  |                                   |')
    ligne7 = list('7 | .   .   .   .   .   .   .   .   . |')
    ligne8 = list('  |                                   |')
    ligne9 = list('6 | .   .   .   .   .   .   .   .   . |')
    ligne10 = list('  |                                   |')
    ligne11 = list('5 | .   .   .   .   .   .   .   .   . |')
    ligne12 = list('  |                                   |')
    ligne13 = list('4 | .   .   .   .   .   .   .   .   . |')
    ligne14 = list('  |                                   |')
    ligne15 = list('3 | .   .   .   .   .   .   .   .   . |')
    ligne16 = list('  |                                   |')
    ligne17 = list('2 | .   .   .   .   .   .   .   .   . |')
    ligne18 = list('  |                                   |')
    ligne19 = list('1 | .   .   .   .   .   .   .   .   . |')
    ligne_avantderniere = '--|-----------------------------------'
    ligne_dernière = '  | 1   2   3   4   5   6   7   8   9'
    tableau = [ligne3, ligne4, ligne5, ligne6, ligne7, ligne8, ligne9, ligne10, ligne11, ligne12, ligne13, ligne14, ligne15, ligne16, ligne17, ligne18, ligne19]
    tableau = tableau[::-1]
    joueurs = état["joueurs"]
    murs = état["murs"]
    murs_vert = murs['verticaux']
    murs_hor = murs['horizontaux']
    noms = []
    positions = []

    for x in joueurs:
        noms += [x['nom']]
        positions += [x['pos']]
    titre += f'Légende: 1={noms[0]}, 2={noms[1]}'

    for x, y in enumerate(positions):
        liste = tableau[y[1] * 2 - 2]
        liste[4 * y[0]] = str(x + 1)
        tableau[y[1] * 2 - 2] = liste

    for i in murs_vert:
        for j in range(3):
            liste = tableau[i[1] * 2 - 2 + j]
            liste[i[0] * 4 - 2] = '|'
            tableau[i[1] * 2 - 2 + j] = liste

    for x in murs_hor:
        for i in range(7):
            liste = tableau[x[1] * 2 - 3]
            liste[x[0] * 4 - 1 + i] = '-'

    tableau = tableau[::-1]
    print(titre)
    print(ligne2)
    for x in tableau:
        chaine = ''.join(x)
        print(chaine)
    print(ligne_avantderniere)
    print(ligne_dernière)


def demande_action(demande, option_reponse):


    action_entre = True
    while action_entre:
        action = input(demande)
        for option in option_reponse:
            if option == action:
                action_entre = False
            if isinstance(option, tuple):
                if option[0] <= action <= option[1]:
                    action_entre = False
    return action

        