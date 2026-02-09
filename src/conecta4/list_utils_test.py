import pytest
from conecta4.list_utils import *
from conecta4.oracle import ColumnClassification, ColumnRecommendation

def test_find():
    needle = 1
    none = [0,0,5,"s"]
    beginning = [1,None,9,6,0,0]
    end = ["x","0",1,1,1]
    several = [0,0,3,4,1,1,3,2,1,3,4]

    assert find_streak(none, needle,1) == False
    assert find_streak(beginning, needle,1)
    assert find_streak(end, needle,3)
    assert find_streak(several, needle,2)

def test_transpose():
    original = [[0,7,3],[4,0,1]]
    transposed = [[0,4],[7,0],[3,1]]

    assert transpose(original) == transposed
    assert transpose(transpose(original)) == original


def test_positive_distance_displace():
    l1 = [1,2,3,4,5,6]
    l2 = [1]
    l3 = [[4,5], ["x", "0","c"]]
    l4 = [9,6,5]

    assert add_prefix([], 2, None) == [None, None]
    assert add_prefix(l1, 2, None) == [None,None, 1,2,3,4,5,6]
    assert add_prefix(l2, 3, "-") == ["-","-","-",1]
    assert add_prefix(l3, 1, "#") == ["#", [4,5], ["x", "0","c"]]
    assert add_prefix(l4,3,0) == [0,0,0,9,6,5]

def test_negative_distance_displace():
    l1 = [1,2,3,4,5,6]
    l2 = [1]
    l3 = [[4,5], ["x", "0","c"]]
    l4 = [9,6,5]

    assert add_suffix([], 2, None) == [None, None]
    assert add_suffix(l1, 2, None) == [1,2,3,4,5,6, None,None]
    assert add_suffix(l2, 3, "-") == [1,"-","-","-"]
    assert add_suffix(l3, 1, "#") == [[4,5], ["x", "0","c"], "#"]
    assert add_suffix(l4,3,0) == [9,6,5,0,0,0,]

def test_displace():
    matrix = [["X",None,None,None],
              ["X",None,None,None],
              ["0","X",None,None],
              ["X","0","X",None]]

    assert (displace_lol(matrix, "-")) == [['-', '-', '-', 'X', None, None, None], 
                                           ['-', '-', 'X', None, None, None, '-'], 
                                           ['-', '0', 'X', None, None, '-', '-'], 
                                           ['X', '0', 'X', None, '-', '-', '-']]


def test_all_same():
    assert all_same([9,1,2,3,4]) == False
    assert all_same([[],[],[]])
    assert all_same([])


    assert all_same([ColumnRecommendation(0, ColumnClassification.LOSE),
                     ColumnRecommendation(2, ColumnClassification.LOSE)])
    
    assert all_same([ColumnRecommendation(0, ColumnClassification.WIN),
                     ColumnRecommendation(0, ColumnClassification.LOSE)]) == False
    

def test_collapse_list():
    assert collapse_list([]) == ""
    assert collapse_list(["0","X","X","0"]) == "0XX0"
    assert collapse_list(["X","X", None, None, None]) == "XX..."

def test_collapse_matrix():
    assert collapse_matrix([]) == ""
    assert collapse_matrix([["X", "X", None], 
                            ["0", "X", "X"], 
                            ["0", None, None]]) == "XX.|0XX|0.."
    
def test_replace_all_in_list():
    assert replace_all_in_list([None, 3, "546", 33, None], None, "#") == ["#", 3, "546", 33, "#"]
    assert replace_all_in_list([1,2,3,4,5], "e", 42) == [1,2,3,4,5]
    assert replace_all_in_list([],34,43) == []

def test_replace_all_in_matrix():
    #caso normal: tiene lo viejo
    assert replace_all_in_matrix([[1,2,3,"n","n", None],
                                  [4,5,"n"]],"n","#") == [[1,2,3,"#","#", None], 
                                                          [4,5,"#"]]
    #caso raro: no tiene lo viejo
    assert replace_all_in_matrix([[None, None, 2, True], 
                                  [4,5,"#"]],"k", 42) == [[None, None, 2, True],
                                                          [4,5,"#"]]
    #caso más raro: lista de listas vacias
    assert replace_all_in_matrix([], None,7) == []
    assert replace_all_in_matrix([[],[]], None, 7) == [[], []]


