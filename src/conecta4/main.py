from conecta4.board import Board
from conecta4.oracle import *
from conecta4.player import Player

from conecta4.list_utils import *

#HORIZONTAL
a = Board()

a.play("X",0)
a.play("X",1)
a.play("X",2)

print(a.prueba_victory("X"))
print(a.print_board(a._columns))

#VERTICAL
matrix_vertical = [["X","X","X",None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
b2 = Board.from_list(matrix_vertical)

print(b2.prueba_victory("X"))
print(b2.print_board(b2._columns))
b = Board()

b.play("X",0)
b.play("X",0)
b.play("X",0)

print(b.prueba_victory("X"))
print(b.print_board(b._columns))

print(b == b2)


#ASCENDENTE
c = Board()

c.play("X",0)
c.play("X",1)
c.play("0",2)
c.play("X",2)
c.play("X",3)
c.play("0",3)
c.play("X",3)

print(c.prueba_victory("X"))
print(c.print_board(c._columns))

#DESCENDENTE
d = Board()

d.play("0",0)
d.play("X",0)
d.play("0",0)
d.play("X",0)
d.play("0",1)
d.play("0",1)
d.play("X",1)
d.play("X",2)
d.play("X",2)


print(d.prueba_victory("X"))
print(d.print_board(d._columns))


#preuba de oráculo
player = Player("Alicia", "X", "0")
e = Board()
e.play("X",0)
e.play("X",1)
e.play("0",2)
e.play("X",2)
e.play("X",3)
e.play("0",3)
#simple = BaseOracle()
recommendation = SmartOracle()
print(recommendation._get_column_recommendation(e, 3, player)._classification)
print(d.print_board(e._columns))
