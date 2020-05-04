import quoridor
import  turtle

class QuoridorX(Quoridor):
    
    def __init__(self, largeur, hauteur):
        super().__init__()
        self.fen = turtle.Screen()
        self.fen.setup(largeur, hauteur)

    def afficher(self):
        fen = turtle.Screen()
        self.fen.title('État actuel du damier de la partie')
        print(self.fen)