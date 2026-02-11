import pytest
from conecta4.game import Game
from conecta4.board import Board

def test_creation():
    g = Game()
    assert g != None

def test_is_game_over():
    game = Game()
    win_x = Board.from_list([["X","0", None, None],
                             ["0","X", None, None],
                             ["X","0", "X", "0"],
                             ["X","0", None, None]])
    
    win_o = Board.from_list([["X","0", "X", "0"],
                             ["X","X", "0", None],
                             ["0","0", None, None],
                             ["0","X", None, None]])
    
    tie = Board.from_list([["0","X", "X", "0"],
                           ["X","0", "0'", "X"],
                           ["0","X", "X", "0"],
                           ["X","0", "0", "X"]])
    
    unfinished = Board.from_list([["0","X", "X", "0"],
                                  [None, None, None, None],
                                  [None, None, None, None],
                                  [None, None, None, None]])

    game.board = win_x
    assert game._has_winner_or_tie()

    game.board = win_o
    assert game._has_winner_or_tie() 

    game.board = tie
    assert game._has_winner_or_tie() 

    game.board = unfinished
    assert game._has_winner_or_tie() == False


