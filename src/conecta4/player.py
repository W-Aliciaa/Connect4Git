

class Player:
    """
    Representa un jugador, con un nombre y un caracter (con el que juega)
    """
    def __init__(self, name:str, char:str, opponent_char:str)->None:
        self._name = name
        self._char = char
        self.opponent_char = opponent_char