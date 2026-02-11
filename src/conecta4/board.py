from conecta4.settings import *
from conecta4.list_utils import *
from copy import deepcopy
from conecta4.string_utils import *


class Board:
    """
    Representa un tablero con las dimensiones de settings
    Detecta una victoria
    """

    #métodos de clase
    @classmethod
    def from_list(cls, list_repr: MatrixColumn):
        board = cls()
        if len(list_repr) != BOARD_COLUMNS:
            raise ValueError("Número de columnas incorrecto")
        board._columns = deepcopy(list_repr)
        return board
    
    @classmethod
    def fromBoardCode(cls, board_code: BoardCode)->Board:
        return cls.fromBoardRawCode(board_code.raw_code)
    
    @classmethod   
    def fromBoardRawCode(cls, board_raw_code: str)-> Board:
        """
        Transforma una cadena en formato de BoardCode en un tablero cuadrado 
        """
        #Convertir la cadena del código en una lista de cadenas
        list_of_strings = board_raw_code.split("|")

        #Transformar cada cadena en una lista de caracteres
        matrix = explode_list_of_strings(list_of_strings)
        
        #Cambiamos todas las ocurrencias de . por None
        matrix = replace_all_in_matrix(matrix, ".", None)
        #Transformamos esa lista en un Board
        return cls.from_list(matrix)

    #dunders
    def __init__(self) -> None:
        """
        Crea un tablero con las dimensiones adecuadas
        El tablero es una "matriz" de caracteres de jugador
        y None representa una posición vacía
        Cada lista es una columna y el fondo es el principio
        """
        self._columns: MatrixColumn = []
        for col_num in range(BOARD_COLUMNS):
            self._columns.append([])
            for row_num in range(BOARD_ROWS):
                self._columns[col_num].append(None)

    def __eq__(self, value: object)->bool:
        """
        Se ejecuta cuando haces a == b
        siendo a`self` y b `value`
        """
        result = False
        if isinstance(value, self.__class__):
            result = (self._columns == value._columns)

        return result
    def __hash__(self)->int:
        return hash(self._columns)
    
    def __repr__(self)->str:
        """
        Devuelve representación textual del objeto: las columnas
        """
        return f"<Board:\n{transpose(self._columns)}>"
    
    def __len__(self):
        return len(self._columns)
    
    def print_board(self, matrix_init: MatrixColumn)->str:
        matrix = transpose(matrix_init)
        new_matrix = ""
        characters = ""
        for sublist in matrix[::-1]:
            for element in sublist:
                if element == None:
                    characters += " - "
                else:
                    characters += " " + element + " "
            new_matrix += str(characters) + "\n"
            characters = ""
        return new_matrix
    
    def as_code(self):
        return BoardCode(self)

    #interfaz pública 
    def play(self, player_char: str, col_number: int)->None:
        """
        Método impuro, solo lleva a cabo efecto secundarios 
        (cambia el tablero)
        Si col_number no es válido, debe de lanzar excepción ValueError
        si la columna está llena o si el indice es de una columna inexistente
        """
        try:
            #selecciono la columna
            col = self._columns[col_number]
            #inserto el char del jugador en el primer None que encuentro
            self.found_slot = False #indica si hemos encontrado un hueco donde meter la jugada
            for index, row in enumerate(col):
                if col[index] == None:
                    self.found_slot = True
                    col[index] = player_char
                    break
                
        except IndexError:
            raise ValueError(f"Ese indice: {col_number}, no es válido")

    def is_tie(self, player_char: str, player2_char:str)->bool:
        """
        No gana ni player1 ni player2, empate
        """
        return (self.is_victory(player_char) and self.is_victory(player2_char)) == False
    
    def is_full(self)->bool:
        """
        Detecta si el tablero está yeno
        """
        return all(None not in column for column in self._columns)

    def is_victory(self, player_char: str)-> bool:
        """
        Determina si hay una victoria para jugador
        representado por un caracter
        """
        return (self._has_vertical_victory(player_char,self._columns) or 
                self._has_horizontal_victory(player_char,self._columns) or
                self._has_ascending_victory(player_char,self._columns) or
                self._has_descending_victory(player_char,self._columns))

    def prueba_victory(self,player_char: str)-> str:
        
        ganador = "NO HAS GANADO!"
        if self._has_vertical_victory(player_char,self._columns):
            ganador = "VICTORIA_VERTICAL" 
        elif self._has_horizontal_victory(player_char,self._columns):
            ganador = "VICTORIA_HORIZONTAL"
        elif self._has_ascending_victory(player_char,self._columns):
            ganador = "VICTORIA_ASCENDENTE"
        elif self._has_descending_victory(player_char,self._columns):
            ganador = "VICTORIA_DESCENDENTE"
        return ganador
    
    
    #interfaz privada
    def _has_vertical_victory(self, player_char: str, matrix: MatrixColumn)->bool:
        result = False
        for column in matrix:
            result = find_streak(column,player_char,VICTORY_STREAK)
            if result:
                break
        return result
                    
    def _has_horizontal_victory(self, player_char: str, matrix: MatrixColumn)->bool:
        invert_matrix = transpose(matrix)
        return self._has_vertical_victory(player_char, invert_matrix)
    
    def _has_ascending_victory(self, player_char: str, matrix: MatrixColumn)->bool:
        extended = displace_lol(matrix, None)
        #print(f"Matriz desplazada{extended}")
        #print(f"Matriz desplazada:\n{self.print_board(extended)}")
        return self._has_horizontal_victory(player_char, extended)
    
    def _has_descending_victory(self, player_char: str, matrix: MatrixColumn)->bool:
        
        #Da la vuelta a cada columna, para que las fichas de arrriba esten abajo, 
        # y entonces sea como una diagonal ascendente
        new_matrix = list(map(lambda fila: fila[::-1], matrix))
        
        #print(f"Matriz transpuesta y desplazada{new_matrix}")
        return self._has_ascending_victory(player_char, new_matrix)
    

#Clase para comprimir el tablero en una cadena,
#para así poder meter el tablero como clave de un diccionario
class BoardCode:
    def __init__(self, board: Board):
        self._raw_code = collapse_matrix(board._columns)

    @property
    def raw_code(self)->str:
        return self._raw_code
    
    def __eq__(self, other: BoardCode)->bool:
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.raw_code == other.raw_code
    
    def __has__(self)->int:
        return hash(self.raw_code)
    
    def __repr__(self)->str:
        return f"{self.__class__}: {self.raw_code}"