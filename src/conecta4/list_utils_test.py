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
    
