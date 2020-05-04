import networkx as nx

class QuoridorError(Exception):
    """ classe pour les raises QuoridorError"""
    pass


class Quoridor:
    """Classe pour encapsuler le jeu Quoridor.
    Attributes:
        état (dict): état du jeu tenu à jour.
        TODO: Identifiez les autres attribut de votre classe
    Examples:
        >>> q.Quoridor()
    """

    def __init__(self, joueurs, murs=None):
        """Constructeur de la classe Quoridor.
        Initialise une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.
        Args:
            joueurs (list): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
                Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
                l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut
                initialement placer 10 murs. Dans le cas où l'argument est un dictionnaire,
                celui-ci doit contenir une clé 'nom' identifiant le joueur, une clé 'murs'
                spécifiant le nombre de murs qu'il peut encore placer, et une clé 'pos' qui
                spécifie sa position (x, y) actuelle.
            murs (dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions (x, y) des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions (x, y) des murs verticaux. Par défaut, il
                n'y a aucun mur placé sur le jeu.
            Raises:
                QuoridorError: L'argument 'joueurs' n'est pas itérable.
                QuoridorError: L'itérable de joueurs en contient un nombre différent de deux.
                QuoridorError: Le nombre de murs qu'un joueur peut placer est plus grand que 10,
                            ou négatif.
                QuoridorError: La position d'un joueur est invalide.
                QuoridorError: L'argument 'murs' n'est pas un dictionnaire lorsque présent.
                QuoridorError: Le total des murs placés et plaçables n'est pas égal à 20.
                QuoridorError: La position d'un mur est invalide.
            """


        liste_joueurs, murs = verification_init(joueurs, murs)

        for i in liste_joueurs:
            if i['murs'] > 10 or i['murs'] < 0:
                raise QuoridorError(f"le nombre de murs qu'un joueur peut placer est >10, ou négatif.")

            elif i['pos'][0] > 9 or i['pos'][0] < 1 or i['pos'][1] > 9 or i['pos'][1] < 1:
                raise QuoridorError(f"la position d'un joueur est invalide.")

        if liste_joueurs[0]['pos'] == liste_joueurs[1]['pos']:
            raise QuoridorError(f"la position d'un joueur est invalide.")

        if (not len(murs['horizontaux']) + len(murs['verticaux']) + liste_joueurs[0]['murs'] + liste_joueurs[1]['murs']) == 20:
            raise QuoridorError(f"le total des murs placés et plaçables n'est pas égal à 20.")

        for x in murs['horizontaux']:
            if x[0] < 2 or x[1] > 8 or x[1] < 1 or x[1] > 9:
                raise QuoridorError(f"QuoridorError: La position d'un mur est invalide.")
        for x in murs['verticaux']:
            if x[0] < 1 or x[1] > 9 or x[1] < 2 or x[1] > 8:
                raise QuoridorError(f"QuoridorError: La position d'un mur est invalide.")

        self.joueurs = liste_joueurs
        self.murs = murs
        self.etat = {'joueurs': self.joueurs, 'murs': self.murs}

    def __str__(self):

        """Représentation en art ascii de l'état actuel de la partie.
        Cette représentation est la même que celle du projet précédent.
        Returns:
            str: La chaîne de caractères de la représentation.
        """

        return self.afficher_damier_ascii()
        # retourne le damier avec l'état actuel de la partie


    def déplacer_jeton(self, joueur, position):

        """Déplace un jeton.
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.
        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).
            position (tuple): Le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.
        """

        if not 1 <= position[0] <= 9 or 1 <= position[1] <= 9:
            raise QuoridorError(f'la position entrée est invalide')

        if joueur == 1:
            self.joueurs[0]['pos'] = (position[0], position[1])
        elif joueur == 2:
            self.joueurs[1]['pos'] = (position[0], position[1])
        else:
            raise QuoridorError(f'le numéro du joueur entré est invalide')


    def état_partie(self):

        """Produire l'état actuel de la partie.
        Returns:
            dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
        Examples:
            {
                'joueurs': [
                    {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                    {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
                ],
                'murs': {
                    'horizontaux': [...],
                    'verticaux': [...],
                }
            }
            où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée
            au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est
            associée à sa position sur le damier. Une position est représentée par un tuple
            de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.
            Les murs actuellement placés sur le damier sont énumérés dans deux listes de
            positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
            est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
            situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
            mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes y et y+1.
        """

        etat = {'joueurs': [{self.joueurs}], 'murs': self.murs}
        return etat


    def jouer_coup(self, joueur):

        """Jouer un coup automatique pour un joueur.
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.
        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).
        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La partie est déjà terminée.

        Returns:
            Tuple[str, Tuple[int, int]]: Un tuple composé du type et de la position du coup joué.
        """

        etat = {'joueurs': self.joueurs, 'murs': self.murs}
        graphe1 = construire_graphe(
            [joueur['pos'] for joueur in etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux']
        )
        if nx.has_path(graphe1, self.joueurs[0]['pos'], 'B1') == False or nx.has_path(graphe1, self.joueurs[1]['pos'], 'B2') == False:
            raise QuoridorError(f'partie terminé, un des 2 joueurs emprisoné')
        if self.joueurs[0]['pos'] == nx.shortest_path(graphe1, self.joueurs[1]['pos'], 'B1')[-2] or self.joueurs[1]['pos'] == nx.shortest_path(graphe1, self.joueurs[1]['pos'], 'B2')[-2]:
            raise QuoridorError(f"un des 2 joueurs est à la case gagnante")
        if joueur == 1:
            if nx.has_path(graphe1, self.joueurs[0]['pos'], 'B1') == True:
                if len(nx.shortest_path(graphe1, self.joueurs[0]['pos'], 'B1')) < len(nx.shortest_path(graphe1, self.joueurs[1]['pos'], 'B2')):
                    return self.déplacer_jeton(1, nx.shortest_path(graphe1, self.joueurs[0]['pos'], 'B1')[1])

            elif len(nx.shortest_path(graphe1, self.joueurs[0]['pos'], 'B1')) > len(nx.shortest_path(graphe1, self.joueurs[1]['pos'], 'B2')):
                return self.placer_mur(1, nx.shortest_path(1, graphe1, self.joueurs[1]['pos'], 'B2')[1], 'horizontaux')
                # on place un mur à la position lui permettant de prendre le chemin le plus court, s'il n'y en avait pas
        if joueur == 2:
            if nx.has_path(graphe1, self.joueurs[1]['pos'], 'B2') == True:
                if len(nx.shortest_path(graphe1, self.joueurs[1]['pos'], 'B2')) < len(nx.shortest_path(graphe1, self.joueurs[0]['pos'], 'B1')):
                    return self.déplacer_jeton(2, nx.shortest_path(graphe1, self.joueurs[1]['pos'], 'B2')[1])
            elif len(nx.shortest_path(graphe1, self.joueurs[1]['pos'], 'B2')) > len(nx.shortest_path(graphe1, self.joueurs[0]['pos'], 'B1')):

                return self.placer_mur(2, nx.shortest_path(graphe1, self.joueurs[0]['pos'], 'B1')[1], 'horizontaux')
                # on place un mur à la position lui permettant de prendre le chemin le plus court, s'il n'y en avait pas


    def partie_terminée(self):

        """Déterminer si la partie est terminée.
        Returns:
            str/bool: Le nom du gagnant si la partie est terminée; False autrement.
        """

        etat = {'joueurs': self.joueurs, 'murs': self.murs}
        graphe1 = construire_graphe(
            [joueur['pos'] for joueur in etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux']
        )

        if self.joueurs[0]['pos'] == nx.shortest_path(graphe1, self.joueurs[0]['pos'], 'B1')[-2]:
            return self.joueurs[0]['nom']

        if self.joueurs[1]['pos'] == nx.shortest_path(graphe1, self.joueurs[1]['pos'], 'B2')[-2]:
            return self.joueurs[1]['nom']


    def afficher_damier_ascii(self):


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
        murs_vert = self.murs['verticaux']
        murs_hor = self.murs['horizontaux']
        positions = []
        joueurs = self.joueurs
        noms = []
        for x in joueurs:
            noms += [x['nom']]
            positions += [x['pos']]
        titre += f'Légende: 1= {noms[0]}, 2= {noms[1]}'

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

        tableau_ascii = ''
        tableau_sub = ''
        tableau_ascii += titre + '\n' + ligne2 + '\n'

        for i in tableau:
            chaine = ''.join(i)
            tableau_sub += chaine + '\n'
        tableau_ascii += tableau_sub[:-1]
        tableau_ascii += '\n' + ligne_avantderniere + '\n' + ligne_dernière + '\n'

        return tableau_ascii

    def placer_mur(self, joueur, position, orientation):

        """Placer un mur.
        Pour le joueur spécifié, placer un mur à la position spécifiée.
        Args:
            joueur (int): le numéro du joueur (1 ou 2).
            position (tuple): le tuple (x, y) de la position du mur.
            orientation (str): l'orientation du mur ('horizontal' ou 'vertical').
        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: La position est invalide pour cette orientation.
            QuoridorError: Le joueur a déjà placé tous ses murs.
        """

        if joueur == 1:
            if orientation == 'horizontaux':
                self.joueurs[0]['murs']['horizontaux'] = (position[0], position[1])

            elif orientation == 'verticaux':
                self.joueurs[0]['murs']['verticaux'] = (position[0], position[1])

        elif joueur == 2:
            if orientation == 'horizontaux':
                self.joueurs[1]['murs']['horizontaux'] = (position[0], position[1])

            elif orientation == 'verticaux':
                self.joueurs[1]['murs']['verticaux'] = (position[0], position[1])

        else:
            raise QuoridorError(f'le numéro du joueur entré est invalide')

def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):

    """Construire un graphe de la grille.
    Crée le graphe des déplacements admissibles pour les joueurs.
    Vous n'avez pas à modifer cette fonction.
    Args:
        joueurs (list): une liste des positions (x,y) des joueurs.
        murs_horizontaux (list): une liste des positions (x,y) des murs horizontaux.
        murs_verticaux (list): une liste des positions (x,y) des murs verticaux.
    Returns:
        DiGraph: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """

    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe

def verification_init(joueurs, murs):

    if not iter(joueurs):
        raise QuoridorError(f"L'argument 'joueurs' n'est pas itérable.")
    if len(joueurs) != 2:
        raise QuoridorError(f"l'itérable de joueurs en contient plus de deux.")
    if murs:
        if not isinstance(murs, dict):
            raise QuoridorError(f"L'argument 'murs' n'est pas un dictionnaire lorsque présent.")
    if not murs:
        murs = {'horizontaux': [], 'verticaux': []}
    liste_joueurs = []
    position_y = 1
    for x in joueurs:
        if isinstance(x, str):
            liste_joueurs.append({'nom': x, 'murs': 10, 'pos': (5, position_y)})
        else:
            liste_joueurs.append(x)
        position_y += 8
    return liste_joueurs, murs