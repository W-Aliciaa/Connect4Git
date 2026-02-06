from conecta4.player import Player
from conecta4.board import Board

class Match():
    def __init__(self, player1: Player, player2: Player):
        player1._char = "X"
        player2._char = "0"
        player1.opponent = player2

        self._players = {player1._char: player1, player2._char: player2}
        self._round_robbin = [player1, player2]

    @property
    def next_player(self) -> Player:
        next = self._round_robbin[0]
        self._round_robbin.reverse()
        return next
    
    def get_player(self, char: str)-> Player:
        return self._players[char]
    
    def get_winner(self, board: Board)-> Player | None:
        """
        Devuelve el jugador ganador y si no lo hay, devulelve None
        """
        winner = None
        if board.is_victory("X"):
            winner = self.get_player("X")
        elif board.is_victory("0"):
            winner = self.get_player("0") 

        return winner