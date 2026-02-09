from conecta4.match import Match
from conecta4.oracle import *
from conecta4.board import Board
from conecta4.player import Player

def test_base_oracle():
    board = Board.from_list([[None,None,None,None],
                             ["x", "o", "x","o"],
                             ["o", "o", "x", "x"],
                             ["o", None, None, None]])
    
    expected = [ColumnRecommendation(0, ColumnClassification.MAYBE),
                ColumnRecommendation(1, ColumnClassification.FULL),
                ColumnRecommendation(2, ColumnClassification.FULL),
                ColumnRecommendation(3, ColumnClassification.MAYBE)]

    rappel = BaseOracle()

    assert len(rappel.get_recommendation(board, None)) == len(expected)
    assert rappel.get_recommendation(board, None) == expected


def test_equality():
    cr = ColumnRecommendation(2, ColumnClassification.MAYBE)

    assert cr == cr #son identicos
    assert cr == ColumnRecommendation(2, ColumnClassification.MAYBE) #equivalentes

    #no equivalentes
    assert cr != ColumnRecommendation(2, ColumnClassification.FULL)
    assert cr != ColumnRecommendation(3, ColumnClassification.FULL)

def test_is_winning_move():
    winner = Player("Xavier", "X")
    loser = Player("Otto", "0")

    empty = Board()
    almost = Board.from_list([["0","X", "0", None],
                              ["0","X", "0", None],
                              ["X", None, None, None],
                              [None, None, None, None]])
    
    oracle = SmartOracle()

    #sobre tablero vacio
    for i in range(0, BOARD_COLUMNS):
        assert oracle._is_winning_move(empty, i, winner) == False
        assert oracle._is_winning_move(empty, i, loser) == False

    #sobre el tablero de verdad
    for i in range(0, BOARD_COLUMNS):
        assert oracle._is_winning_move(almost, i, loser) == False

    assert oracle._is_winning_move(almost, 2, winner)


"""
def test_is_loosing_move():
    winner = Player("Xavier")
    loser = Player("Otto")
    match = Match(loser,winner)

    # Confirma que los oponentes están bien
    assert winner.opponent == loser
    assert loser.opponent == winner

    # Confirma los chars
    assert winner._char == "0"  # por cómo Match los asigna
    assert loser._char == "X"

    empty = Board()
    almost = Board.from_list([["0","X", "0", None],
                              ["0","X", "0", None],
                              ["X", None, None, None],
                              [None, None, None, None]])
    
    oracle = SmartOracle()

    #sobre tablero vacio
    for i in range(0, BOARD_COLUMNS):
        assert oracle._is_losing_move(empty, i, winner) == False
        assert oracle._is_losing_move(empty, i, loser) == False

    #sobre el tablero de verdad
    assert oracle._is_losing_move(almost, 3, winner)

    assert oracle._is_losing_move(almost, 2, loser) == False

"""