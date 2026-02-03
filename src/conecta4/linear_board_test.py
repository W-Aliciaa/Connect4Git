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
