from conecta4.oracle import SmartOracle,ColumnClassification, ColumnRecommendation
from conecta4.board import Board

class Player:
    """
    Representa un jugador, con un nombre y un caracter (con el que juega)
    """
    def __init__(self, name:str, char:str = None, opponent: Player = None)->None:
        self._name = name
        self._char = char
        self.opponent = opponent
        self._oracle = SmartOracle()

    @property
    def opponent(self):
        return self._opponent
    
    @opponent.setter
    def opponent(self, other: Player):
        if other != None:
            self._opponent = other
            other._opponent = self

    def play(self, board: Board)->None:
        """
        Elige la mejor columna de aquellas que recomienda el oráculo
        """
        # Pregunta al oráculo
        (best, recommendations) = self._ask_oracle(board)
        if best == None:
           if board.is_tie(self._char, self.opponent._char):
               print("EMPATE")
        else:
            board.play(self._char, best.index)


    def _ask_oracle(self, board, position):
        """
        Pregunta al oráculo y devuelve la mejor opción
        """
        #obtenemos las recomendaciones
        recomendations = self._oracle.get_recommendation(board, self)
        #seleccionamos la mejor
        best = self._choose(recomendations)

        return (best, recomendations)

    def _choose(self, recomendations: list[ColumnRecommendation])->ColumnRecommendation:
        """
        Selecciona la mejor opción de la lista
        de recomendaciones
        """
        #quitamos las no validas
        valid = list(filter(lambda x: x.classification != ColumnClassification.FULL, recomendations))
        #pillamos la primera de las válidas
        return valid[0]

class HumanPlayer(Player):

    def __init__(self, name, char = None):
        super().__init__(name, char)
    def _ask_oracle(self, board):
        """
        Le pido al humano que es mi oráculo
        """
        while True:
            #pedimos columna al humano
            raw = input("Select a column, puny human (or h for help): ")
            movement = ()
            #verificamos que su respuesta no sea una idiotez
            if self._is_int(raw) and self._is_within_column_range(board, int(raw)) and self._is_non_full_column(board, int(raw)): 
                #si no lo es, jugamos donde ha dicho y salimos del bucle
                pos = int(raw)
                movement = (ColumnRecommendation(pos, None), None)
                break
            elif raw.lower() == "h":
                #imprimir las recomendaciones de donde poner la siguiente ficha (donde sería mejor jugar)
                print(self._oracle.get_recommendation(board,self))
        return movement
    

#funciones de validación de índice de columna
def is_non_full_column(board: Board, num: int)-> bool:
    return None in  board._columns[num]
        
def is_within_column_range(board: Board, num: int)-> bool:
    return num >= 0 and num < len(board)

def is_int(string: str)->bool:
    try:
        num = int(string)
        return True
            
    except:
        return False
