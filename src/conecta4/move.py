from conecta4.board import BoardCode
from conecta4.oracle import ColumnRecommendation
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from conecta4.player import Player


class Move:

    def __init__(self, position: int, board_code: BoardCode, recomendations: list[ColumnRecommendation], player: Player)->None:
        self.position = position
        self.board_code = board_code
        self.recomendtaions = recomendations
        self.player = player