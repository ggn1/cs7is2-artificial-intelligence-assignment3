### This file contains common functions that all files can use.
import time
import traceback
import numpy as np
from datetime import datetime
from typing import Callable, Dict

def get_datetime_id(dt:datetime=None) -> str:
    """
    Converts a given datetime object into 
    a string identifier.
    @param dt: Datetime object. If this is None
               considered it to be current date time.
    @param: String DayMonthYearHourMinSecond
    """
    if dt is None: dt = datetime.now()
    return (
        str(dt.day).zfill(2) 
        + str(dt.month).zfill(2) 
        + str(dt.year).zfill(2)
        + str(dt.hour).zfill(2) 
        + str(dt.minute).zfill(2) 
        + str(dt.second).zfill(2)
    )

def track_time(f:Callable):
    """
    This function will return a wrapper function
    that computes and returns execution time
    and the value returned by the executed function.
    @param f: Function whose execution time
                is to be measured.
    @return: Execution time in seconds.
    """
    def wrapper(*args, **kwargs):
        to_return = {'f_out': None, 'seconds': 0}
        time_start = time.time() # keep track of time
        try:
            try:
                res = f(*args, **kwargs)
                to_return['f_out'] = res 
            except Exception as e:
                print(f"Exception! {f.__name__}(...): {e}")
                print(traceback.format_exc())
        except KeyboardInterrupt:
            print(f"Keyboard Interrupt! {f.__name__}(...)")
        finally:
            to_return['seconds'] = time.time() - time_start 
        return to_return
    return wrapper

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

def state_str_to_num(state_str:np.ndarray, sym_map:Dict[str, int]) -> list:
    """
    Given a state with symbols as string,
    returns one with symbols replaced by
    numbers as per given mapping.
    @param state_str: Given state with string elements.
    @param sym_map: A mapping of string symbol to
                    desired number.
    """
    for k, v in sym_map.items():
        state_str[state_str == k] = str(v)
    state_num = state_str.astype(int)
    return state_num.tolist()

def state_num_to_str(state_num:np.ndarray, sym_map:Dict[int, str]) -> list:
    """
    Given a state with symbols as numbers,
    returns one with symbols replaced by
    strings as per given mapping.
    @param state_str: Given state with string elements.
    @param sym_map: A mapping of integer to 
                    desired string symbol.
    """
    state_str = state_num.astype(str)
    for k, v in sym_map.items():
        state_str[state_str == str(k)] = v
    return state_str.tolist()
   
def get_opposite_symbol(sym:str) -> str:
    """ 
    Given a symbol, get's that of the opponent. 
    @param sym: This player's symbol.
    @return: Opponent's symbol.
    """
    if sym == "X": return "O"
    elif sym == "O": return "X"
    elif sym == 'R': return "Y"
    elif sym == "Y": return "R"
    raise Exception(f"Invalid symbol '{sym}'.")