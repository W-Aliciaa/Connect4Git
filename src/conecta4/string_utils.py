def explode_string(string: str)->list[str]:
    """
    Transforma una cadena en una lista de caracteres
    """
    return list(string)

def explode_list_of_strings(list_strings: list[str])->list[list[str]]:
    """
    Aplica explode_string a cada cadena de la lista
    """
    matrix = []
    for s in list_strings:
        matrix.append(explode_string(s))
    return matrix