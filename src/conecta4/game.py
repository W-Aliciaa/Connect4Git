import pyfiglet
from enum import Enum, auto
from conecta4.oracle import BaseOracle, LearningOracle, SmartOracle
from conecta4.player import Player, HumanPlayer, ReportingPlayer
from conecta4.match import Match
from conecta4.board import Board
from conecta4.list_utils import transpose
from beautifultable import BeautifulTable
from conecta4.settings import *

class RoundType(Enum):
    COMPUTER_VS_COMPUTER = auto()
    COMPUTER_VS_HUMAN = auto()

class DifficultyLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class Game:
    def __init__(self, round_type: RoundType = RoundType.COMPUTER_VS_COMPUTER, match: Match = Match(ReportingPlayer("Chip"), ReportingPlayer("Chop")))-> None:
        #Guardar valores recibidos
        self.round_type = round_type
        self.match = match
        
        #tablero vacio sobre el que jugar
        self.board = Board()


    def start(self)-> None:
        #imprimo el nombre o logo del juego
        self.print_logo()
        #configuro la partida
        self._configure_by_user()
        #arrancho el game loop
        self._start_game_loop()

    def print_logo(self)-> None:
        logo = pyfiglet.Figlet(font ="stop")
        print(logo.renderText("Connecta"))

    def _start_game_loop(self)-> None:
        #bucle infinito
        while True:
            #obtengo el jugador de turno
            current_player = self.match.next_player
            #le hago jugar
            current_player.play(self.board)
            #muestro su jugada
            self._dispplay_move(current_player)
            #imprimo el tablero
            self._display_board()
            #si hay vencedor o empate
            if self._has_winner_or_tie():
                #muestro resultado final
                self._display_result()

                if self.match.is_match_over():
                    #se acabo el juego, salgo del bucle
                    break
                else:
                    #reseteamos el tablero
                    self.board = Board()
                    self._display_board()



    def _dispplay_move(self, player: Player)-> None:
        print(f"\n{player._name} ({player._char}) has moved in column #{player.last_moves[0].position}")

    def _display_board(self):
        """
        Imprimir el tablero
        """
        #obtenemos una matriz de caracteres a partir del tablero
        matrix = transpose(self.board._columns)
        matrix = matrix[::-1]
        matrix = transpose(matrix)
        
        #crear la tabla de beautifultable
        bt = BeautifulTable()
        for col in matrix:
            bt.columns.append(col)
        bt.columns.header = [str(i) for i in range(BOARD_COLUMNS)]
        #imprimirla
        print(bt)

    def _display_result(self)-> None:
        winner = self.match.get_winner(self.board)
        if winner != None:
            print(f"\n{winner._name} ({winner._char}) wins!!!")
        else:
            print(f"\nA tie between {self.match.get_player("X").name} (X) and {self.match.get_player("0").name} (0)")

    def _has_winner_or_tie(self)-> bool:
        winner = self.match.get_winner(self.board)
        over = False
        if winner != None:
            #hay vencedor
            winner.on_win()
            winner.opponent.on_lose()
            over = True
        elif self.board.is_full():
            #lleno / empate
            over = True
            
        return over


    def _configure_by_user(self)-> None:
        """
        Le pido al usuario, los valores que ÉL quiere para tipo de partida
        y nivel de dificultad
        """

        #determinar el tipo de partida (preguntando al usuario)
        self.round_type = self._get_round_type()

        if self.round_type == RoundType.COMPUTER_VS_HUMAN:
            #preguntamos nivel de dificultad
            self._difficulty_level = self._get_difficulty_level()

        #crea la partida
        self.match = self._make_match()

    def _get_difficulty_level(self):
        """
        Pregunta al usuario como de listo quiere que sea su oponente
        """
        print("""
            Chose your opponent, human:
              1) Easy: for clowns and wimps
              2) Difficult: you may regret it
              3) Hard: Don't even think about it!
              """)
        while True:
            response = input("Please type 1, 2 or 3: ").strip()
            if response == "1":
                level = DifficultyLevel.LOW
                break
            elif response == "2":
                level = DifficultyLevel.MEDIUM
                break
            else:
                level = DifficultyLevel.HIGH
                break
        return level

    def _get_round_type(self)-> RoundType:
        """
        Preguntamos al usuario tipo de partida
        """
        print("""
              Select type of round:
              
              1) Computer vs Computer
              2) Computer vs Human
              """)
        response = ""
        while response != "1" and response != "2":
            response = input("Please type either 1 or 2: ")
        
        if response == "1":
            return RoundType.COMPUTER_VS_COMPUTER
        else:
            return RoundType.COMPUTER_VS_HUMAN
        
    def _make_match(self)-> Match:
        """
        Player 1 siempre robótico
        """
        _levels = {DifficultyLevel.LOW : BaseOracle(),
                   DifficultyLevel.MEDIUM: SmartOracle(),
                   DifficultyLevel.HIGH: LearningOracle()}
        
        if self.round_type == RoundType.COMPUTER_VS_COMPUTER:
            #ambos jugadores robóticos
            player1 = ReportingPlayer("T-X", oracle = LearningOracle())
            player2 = ReportingPlayer("T-1000", oracle = LearningOracle())
        else:
            # ordenador vs humano
            player1 = ReportingPlayer("T-800", oracle = _levels[self._difficulty_level])
            player2 = HumanPlayer(name = input("Enter your name, human: "))

        return Match(player1,player2)