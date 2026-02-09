from conecta4.oracle import BaseOracle,SmartOracle,ColumnClassification, ColumnRecommendation
from conecta4.board import Board
from conecta4.list_utils import all_same
import random


class Player:
    """
    Representa un jugador, con un nombre y un caracter (con el que juega)
    """
    def __init__(self, name:str, char:str = None, opponent: Player = None, oracle = SmartOracle())->None:
        self._name = name
        self._char = char
        self._opponent = None
        self.opponent = opponent
        self._oracle = oracle
        self.last_move = None
        

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

        #juego en la mejor
        self._play_on(board, best._index)

    def _play_on(self, board, position):
            #juega en la pos
            board.play(self._char, position)
            #Guardo mi jugada
            self.last_move = position


    def _ask_oracle(self, board):
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
        choice = ColumnClassification.MAYBE
        #quitamos las no validas
        valid = list(filter(lambda x: x._classification != ColumnClassification.FULL, recomendations))
        #ordenamos por mejor a peor clasificación
        valid = sorted(valid,key = lambda x: x._classification.value, reverse = True)
        #si son todas iguales, pillo una al azar
        if all_same(valid):
            choice = random.choice(valid)
        
        else:
            #si no lo son, pillo la más deseable (que será la primera)
            choice = valid[0]
    
        return choice

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
    def _is_non_full_column(self,board: Board, num: int)-> bool:
        return None in  board._columns[num]
        
    def _is_within_column_range(self,board: Board, num: int)-> bool:
        return num >= 0 and num < len(board)

    def _is_int(self,string: str)->bool:
        try:
            num = int(string)
            return True  
        except:
            return False
    



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
