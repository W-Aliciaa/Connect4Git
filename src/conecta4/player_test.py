import pytest
from conecta4.player import *
from conecta4.oracle import *
from conecta4.board import Board

def test_play():

    """
    Comprobamos que se juega en la primera columna disponible
    """

    before = Board.from_list([[None,None,None,None],
                             ["x", "o", "x","o"],
                             ["x", "o", "x", "o"],
                             ["x", None, None, None]])
    
    after = Board.from_list([["x",None,None,None],
                             ["x", "o", "x","o"],
                             ["x", "o", "x", "o"],
                             ["x", None, None, None]])
    
    player = Player("Chip", "x")
    before.play("x",0)
    recommendation = BaseOracle()
    assert recommendation._get_column_recommendation(before,0,player)._classification == ColumnClassification.MAYBE
    assert recommendation._get_column_recommendation(before,1,player)._classification == ColumnClassification.FULL
    assert before == after


def test_valid_column():
    board = Board.from_list([["x",None,None,None],
                            ["x", "o", "x","o"],
                            ["o", "o", "x", "x"],
                            ["o", None, None, None]])
        
    assert is_within_column_range(board,0)
    assert is_within_column_range(board,1)
    assert is_within_column_range(board,2)
    assert is_within_column_range(board,3)
    assert is_within_column_range(board,5) == False
    assert is_within_column_range(board,-10) == False
    assert is_within_column_range(board,10) == False

def test_is_non_full_column():
    board = Board.from_list([["x",None,None,None],
                            ["x", "o", "x","o"],
                            ["o", "o", "x", "x"],
                            ["o", None, None, None]])
        
    assert is_non_full_column(board,0)
    assert is_non_full_column(board,1) == False
    assert is_non_full_column(board,2) == False
    assert is_non_full_column(board,3)

def test_is_int():
    assert is_int("42")
    assert is_int("0")
    assert is_int("-32")
    assert is_int("  32  ")
    assert is_int("hola") == False
    assert is_int("") == False
    assert is_int("3.14") == False

