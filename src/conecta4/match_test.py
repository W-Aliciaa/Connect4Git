import pytest
from conecta4.player import Player, HumanPlayer
from conecta4.match import Match

xavier = None
otto = None

#setup_function() y teardown_function() se utilizan para que cada vez que se llame a 
#las variables globales xavier y otto dentro de cada función se creen nuevas
def setup_function():
    global xavier
    xavier = HumanPlayer("Prof.Xavier")
    global otto
    otto = Player("Dr Octopus")

def teardown_function():
    global xavier
    xavier = None
    global otto
    otto = None


def test_different_players_have_different_chars():
    t = Match(xavier,otto)
    assert xavier._char != otto._char

def test_no_player_with_none_char():
    t = Match(xavier, otto)
    assert xavier._char != None
    assert otto._char != None

def test_next_player_is_round_robbin():
    t = Match(otto, xavier)
    p1 = t.next_player
    p2 = t.next_player
    assert p1 != p2

def test_players_are_opponents():
    t = Match(otto, xavier)
    p1 = t.get_player("X")
    p2 = t.get_player("0")
    assert p1.opponent == p2
    assert p2.opponent == p1
