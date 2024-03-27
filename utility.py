### This file contains common functions that all files can use.

def print_debug(to_print):
    """ 
    Prints the statement with a "[DEBUG]" 
    string attached to the front.
    @param to_print: Content to print.
    """
    print("[DEBUG]", to_print)

def list_to_tuple_2d(l:list) -> tuple:
    """
    Converts given 2D list to a 2D tuple.
    @param l: List to convert.
    @return: 2D tuple.
    """
    return tuple([tuple(row) for row in l])

def tuple_to_list_2d(t:tuple) -> list:
    """
    Converts given 2D tuple to a 2D list.
    @param t: Tuple to convert.
    @return: 2D list.
    """
    return [list(e) for e in t]
