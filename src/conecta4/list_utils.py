from conecta4.settings import *
from typing import Any

def find_streak(haystack, needle, streak):
  assert streak > 0
  contador = 0
  for element in haystack:
    if element == needle:
      contador += 1
      if contador == streak:
        break
    else:
      #este es opcional se puede quitar ya que es implicito, si no es igual a la
      #aguja se queda en falso y contador se resetea a 0
      contador = 0
      
  return contador == streak

def get_nths(matrix: MatrixColumn, n):
  """
  Recibe un matriz y devuelve una lista con el elemento en la posición n de cada sublista
  Si la sublista no tiene indice n coloca None
  """
  result = []  

  # recorremos cada sublista dentro de la matriz
  for sublist in matrix:
    if n < len(sublist):
      value = sublist[n]   # sí existe cogemos el valor
    else:
      value = None         # si no ponemos None

    result.append(value)     

  return result


def transpose(matrix: MatrixColumn) -> MatrixColumn:
  """
  Devuelve la matriz transpuesta usando get_nths.
  Convierte columnas en filas.
  """
  transposed = []
  # Compruebo si existe y no esta vacia
  if matrix and matrix[0]:
    # Repito tantas veces como elementos tiene la primera fila (o columna) de la matriz  
    for element in range(len(matrix[0])): 
      # Añado  
      transposed.append(get_nths(matrix, element))

  return transposed

def add_prefix(elements:list, number: int, filler: Any)->Any:
  """
  recibe una lista y devuelve una nueva lista con number rellenos 
  al principio (un prefijo):
  add_prefix([1,2], 2, None) -> [None, None, 1,2]
  """
  return ([filler] * number) + elements

def add_suffix(elements:list, number: int, filler: Any)->Any:
  """
  recibe una lista y devuelve una nueva lista con number rellenos 
  al final (un sufijo):
  add_suffix([1,2], 2, None) -> [1,2, None, None]
  """
  return elements + ([filler] * number)

def displace_list(elements: list, distance: int, total_size: int, filler: Any)->list:
  """
  Crea una nueva lista de tamaño total_size, con la original, desplazada
  hacia en final distance posiciones.
  Los espacios nueos se rellenan con filler
  displace_list([1,2,3], 1, 7, None) -> [None, 1, 2, 3, None, None, None]
  """
  prefix_added = add_prefix(elements, total_size, filler)
  return  add_suffix(prefix_added, distance, filler)

def displace_lol(matrix: MatrixColumn,filler: Any):
  """
  Aplica displace_list a cada sublista del lol y devuelve un nuevo lol
  """
  #print(f'original {matrix}')

  extended = []
  size = len(matrix[0])-1
  for index, col in enumerate(matrix):
    extended.append(displace_list(col, index, size, filler))
    size -= 1

  return extended