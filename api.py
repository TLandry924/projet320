import requests


url_base = 'https://python.gel.ulaval.ca/quoridor/api/'

def lister_parties(idul):
    rep = requests.get(url_base+'lister/', params={'idul': idul})
    if rep.status_code == 200:
        reponse = rep.json()
    print(rep)
    if rep.status_code != 200:
        raise RuntimeError(f"Le GET sur {url_base+'lister'} a produit le code d'erreur {rep.status_code}.")
    return reponse['parties']

def débuter_partie(idul):
    rep = requests.post(url_base+'débuter/', data={'idul': idul})
    if rep.status_code == 200:
        reponse = rep.json()
        return reponse['id'], reponse['état']

    else:
        raise RuntimeError(f"le POST sur {url_base+'débuter'} a produit le code d'erreur {rep.status_code}.")

def jouer_coup(id_partie, type_coup, position):
    rep = requests.post(url_base+'jouer/', data={'id': id_partie, 'type': type_coup, 'pos':
    position})
    if rep.status_code == 200:
        reponse = rep.json()
        if 'gagnant' in reponse:
            raise StopIteration(f"Le vainqueur est {reponse['gagnant']}")
        if 'message' in reponse:
            raise RuntimeError(f"Le vainqueur est {reponse['message']}")
        if 'état' in reponse:
            return reponse('état')

    else:
        raise RuntimeError(f"le POST sur {url_base+'jouer'} a produit le code d'erreur {rep.status_code}.")