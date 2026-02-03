import pytest
from conecta4.board import *
from conecta4.settings import BOARD_COLUMNS,VICTORY_STREAK

def test_empty_board():
    empty = Board()
    assert empty != None
    assert empty.is_full() == False
    assert empty.is_victory("X") == False

def test_play():
    b = Board()
    for i in range(BOARD_COLUMNS):
        b.play("X",i)
    assert b.is_full() == True

def test_victory():
    b = Board()
    for i in range(VICTORY_STREAK):
        b.play("X",i)
    
    assert b.is_victory("0") == False
    assert b.is_victory("X") == True

def test_tie(): #empate de columna
    b = Board()

    b.play("0",1)
    b.play("0",1)
    b.play("X",1)
    b.play("0",1)

    assert b.is_tie("X","0")

def test_add_to_full():
    full = Board()
    for i in range(BOARD_COLUMNS):
        full.play("X",i)
    full.play("X",BOARD_COLUMNS-1)
    assert full.is_full()

def test_vertical_victory():
    vertical = Board.from_list([["X","X","X",None],
                               [None,None,None,None],
                               [None,None,None,None],
                               [None,None,None,None]])
    
    assert vertical.prueba_victory("X") == "VICTORIA_VERTICAL"
    assert vertical.prueba_victory("0") == "NO HAS GANADO!"

def test_horizontal_victory():
    horizontal_victory = Board.from_list([[None,"X",None,None],
                                         [None,"X",None,None],
                                         [None,"X",None,None],
                                         [None,None,None,None]])
    
    assert horizontal_victory.prueba_victory("X") == "VICTORIA_HORIZONTAL"
    assert horizontal_victory.prueba_victory("0") ==  "NO HAS GANADO!"

def test_ascendent_victory():
    ascendent_victory = Board.from_list([[None,"X",None,None],
                                         [None,None,"X",None],
                                         [None,None,None,"X"],
                                         [None,None,None,None]])
    assert ascendent_victory.prueba_victory("X") == "VICTORIA_ASCENDENTE"
    assert ascendent_victory.prueba_victory("0") ==  "NO HAS GANADO!"

def test_descendent_victory():
    descendent_victory = Board.from_list([[None,None,None,"X"],
                                         [None,None,"X",None],
                                         [None,"X",None,None],
                                         ["X",None,None,None]])
    
    assert descendent_victory.prueba_victory("X") == "VICTORIA_DESCENDENTE"
    assert descendent_victory.prueba_victory("0") ==  "NO HAS GANADO!"