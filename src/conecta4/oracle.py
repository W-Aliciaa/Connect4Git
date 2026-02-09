from typing import TYPE_CHECKING
from enum import Enum, auto
from conecta4.board import Board
from conecta4.settings import BOARD_COLUMNS, BOARD_ROWS
from copy import deepcopy
if TYPE_CHECKING:
    from conecta4.player import Player, HumanPlayer

#Clases de columna
class ColumnClassification(Enum):
    FULL = -1   # Imposible
    LOSE =  5  # Derrota inminente
    BAD  = 10  # Muy indeseable
    MAYBE = 20  # Indeseable (no se muy bien que va a pasar, mejor no arriesgar)
    WIN  = 100  # Victoria inmediata

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
            return self._classification == other._classification
    
    def __hash__(self)->int:
        return hash((self._index, self._classification))
    

    def __repr__(self)->str:
        """
        Devuelve representación textual de las recomendaciones
        """
        return f"Recomendationes: {self._classification}"
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

    def get_recommendation(self, board: Board, player: "Player | HumanPlayer")->list[ColumnRecommendation]:
        recomendations = []
        for index in range(BOARD_COLUMNS):
            recomendations.append(self._get_column_recommendation(board,index,player))
        return recomendations
        

    def _get_column_recommendation(self, board: Board, index: int, player: "Player")->ColumnRecommendation:
        """
        Método privado, que determina si una columna está llena, en cuyo caso la clasifica
        como FULL, para todo lo demás, MAYBE
        """

        result = ColumnRecommendation(index, ColumnClassification.MAYBE)

        # compruebo si me he equivocado, y si es asi, cambio el valor de result
        last_element = len(board._columns[index])-1
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
                                  player: "Player")-> ColumnRecommendation:
        
        """
        Afinar las recomendaciones. Las que hayan salido como MAYBE,
        intento ver si hay algo más preciso, en concreto una victoria
        para player.
        """
        #pido la clasificación básica
        recommendation = super()._get_column_recommendation(board, index, player)
    
        #Afino los Maybe: juego como player en esa columna y compruebo si eso me da una victoria
        if recommendation._classification == ColumnClassification.MAYBE:
            if self._is_winning_move(board, index, player):
                recommendation._classification = ColumnClassification.WIN
            elif self._is_losing_move(board, index, player):
                recommendation._classification = ColumnClassification.LOSE
            
        return recommendation
    
    def _is_losing_move(self, board: Board, index: int, player: Player)->bool:
        """
        Si player juega en index, genera una jugada vencedora para el
        oponente en alguna de las demás columnas?
        """
        temp_board = self._play_on_temp_board(board, index, player)
        will_lose = False
        for i in range(0, BOARD_COLUMNS):
            if self._is_winning_move(temp_board, i, player.opponent):
                will_lose = True
                break
        return will_lose

    def _is_winning_move(self, board: Board, index: int, player: "Player")->bool:
        """
        Determina si al jugar en una posición, nos llevaría a gnar de inmediato
        """
        #hago una copia del tablero
        #juego en ella
        temp_board = self._play_on_temp_board(board, index, player)
        #determino si hay una victoria para player o no
        return temp_board.is_victory(player._char)

    def _play_on_temp_board(self, original: Board, index: int, player: "Player")->Board:
        """
        Crea una copia (profunda) del board original juega en nombre de player
        en la columna que nos han dicho, y devuelve el board resultante
        """
        board_temp = deepcopy(original)
        board_temp.play(player._char, index)
        return board_temp
