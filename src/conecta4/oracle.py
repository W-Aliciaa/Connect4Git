from enum import Enum, auto
from conecta4.board import Board
from conecta4.player import Player
from conecta4.settings import BOARD_COLUMNS, BOARD_ROWS
from copy import deepcopy

#Clases de columna
class ColumnClassification(Enum):
    FULL = auto()   # Imposible
    LOSE = auto()   # Derrota inminente
    BAD  = auto()   # Muy indeseable
    MAYBE = auto()  # Indeseable (no se muy bien que va a pasar, mejor no arriesgar)
    WIN  = auto()   # Victoria inmediata

#Recomendación de una columna: indice + clase
class ColumnRecommendation: 
    """
    Clase que representa la recomendación del oráculo para
    una columna. Se compone del índice de dicha columna en el 
    tablero y un valor de ColumnClassification.
    """

    def __init__(self, index: int, classification: ColumnClassification)-> None:

        self._index = index
        self._classification = classification

    def __eq__(self,other)->bool:
        #si son de clases distintas, pues distintos
        if not isinstance(other, self.__class__):
            return False
        else:
            return (self._index, self._classification) == (other._index, other._classification)ç
    
    def __hash__(self)->int:
        return hash((self._index, self._classification))
# Oráculos, de más tonto a más listo

#Los oráculos, deben de realizar un trabajo complejo: clasificar columnas
#en el caso más complejo, teniendo en cuenta errores del pasado.
#Usamos divide y vencerás, y cada oráculo, del más tonto al más listo
#se encargará de una parte.
class BaseOracle:
    """
    La clase base y el oráculo más tonto: clasifica las columnas en llenas
    y no llenas.
    """

    def get_recommendation(self, board: Board, player: Player )->list[ColumnRecommendation]:
        recomendations = []
        for index in range(BOARD_COLUMNS):
            recomendations.append(self._get_column_recommendation(board,index,player))
        return recomendations
        

    def _get_column_recommendation(self, board: Board, index: int, player: Player)->ColumnRecommendation:
        """
        Método privado, que determina si una columna está llena, en cuyo caso la clasifica
        como FULL, para todo lo demás, MAYBE
        """

        result = ColumnRecommendation(index, ColumnClassification.MAYBE)

        # compruebo si me he equivocado, y si es asi, cambio el valor de result
        last_element = BOARD_ROWS - 1 #len(board._columns[index]) -1
        if board._columns[index][last_element] != None:
            result = ColumnRecommendation(index, ColumnClassification.FULL)

        return result

class SmartOracle(BaseOracle):
    """
    Refina la recomendación del oráculo base, intentando afinar la
    clasificación MAYBE a algo más preciso. En concreto a WIN: va a determinar
    que jugadas nos llevan a ganar de inmediato
    """

    def _get_column_recommendation(self,
                                  board: Board,
                                  index: int,
                                  player: Player)-> ColumnRecommendation:
        
        """
        Afinar las recomendaciones. Las que hayan salido como MAYBE,
        intento ver si hay algo más preciso, en concreto una victoria
        para player.
        """
        #pido la clasificación básica
        recommendation = super()._get_column_recommendation(board, index, player)
        #tablero temporal
        
        #Afino los Maybe: juego como player en esa columna y compruebo si eso me da una victoria
        if recommendation._classification == ColumnClassification.MAYBE:
            #creo un tablero temporal a partir de board
            #juego en index
            temp_board = self._play_on_temp_board(board, index, player, player._char)
            temp_board_play2 = self._play_on_temp_board(board, index, player, player.opponent_char)

            #le pregunto al tablero temporal si is_victory(player)
            if temp_board.is_victory(player._char):
                #si es así, reclasifico a WIN
                recommendation._classification = ColumnClassification.WIN
                recommendation._index = index
            elif temp_board_play2.is_victory(player.opponent_char):
                recommendation._classification = ColumnClassification.LOSE
                recommendation._index = index
        return recommendation
    

    def _play_on_temp_board(self, original: Board, index: int, player: Player, player_char: str)->Board:
        """
        Crea una copia (profunda) del board original juega en nombre de player
        en la columna que nos han dicho, y devuelve el board resultante
        """
        board_temp = deepcopy(original)
        if player_char == player.opponent_char:
            for i in range(BOARD_COLUMNS):
                board_temp.play(player_char, i)
        else:
            board_temp.play(player_char, index)
        return board_temp
