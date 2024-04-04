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

def get_player_perspective(board:np.ndarray, sym:str):
    """
    Returns the numeric state of a given board from the
    perspective of a given player.
    @param board: Given board.
    @param sym: Symbol of given player.
    @return: The given player's perspective
             with own pieces = 1, opponent's pieces = 0,
             and spaces = -1.
    """
    sym_me = sym
    sym_opponent = get_opposite_symbol(sym)
    char_to_int = {sym_me: 1, sym_opponent: 0, "#": -1}
    board = board.to_list() # Board containing characters.
    player_view = np.array([
        [char_to_int[char] for char in row] 
        for row in board
    ])
    return player_view

def get_world_perspective(
    num_board:np.ndarray, 
    sym:str,
):
    """
    Returns the numeric state of a given board from the
    perspective of a given player.
    @param num_board: Given board with numbers as per a
                      particular player's perspective.
    @param sym: Symbol of the player who's perspective 
                given board is from.
    @return: The board where this player's pieces
             are replaced with given symbol,
             and their opponent's is replaced
             by the opposite symbol and spaces are #.
    """
    sym_me = sym
    sym_opponent = get_opposite_symbol(sym)
    int_to_char = {1: sym_me, 0: sym_opponent, -1:"#"}
    board = num_board.to_list() # Board containing characters.
    world_view = np.array([
        [int_to_char[i] for i in row] 
        for row in board
    ])
    return world_view

def get_random_num_board(board_size:tuple) -> np.ndarray:
    """ 
    Returns a random board (need not be valid) 
    for given board size populated with numbers 
    mimicking a specific player's perspective.
    @param board_size: Size of the board.
    @return board: Board as numpy array.
    """
    board_rand = np.random.randint(0, 3, size=board_size)
    board_rand[board_rand == 2] = -1
    return board_rand

def odd_or_even(number:int) -> int:
    """
    Check if a number is odd.
    @param number: Number to check.
    @return: Number 1 if number is odd and 0
             if it is even.
    """
    return int(number % 2 != 0)

def board2int(num_board:np.ndarray) -> int:
    """
    Converts binary string into an integer.
    This is by first obtaining an 85 bit long
    bit string that's representative of the 
    game board and then converting this bit 
    string into a number. The the first 42 bits 
    correspond to whether a piece at each position of 
    the 2D board flattened into a 1D list is a [1] piece 
    or a [0] piece with 1 => [1] and 0 => [0]. 
    The next set of 42 bits indicate whether the position 
    on tbe board is a free space or a piece with 0 => space 
    and 1 => piece.
    @param num_board: Game board from the perspective
                      of a particular player.
    @return: Game board as an integer.
    """
    spaces = ""
    symbols = ""
    for n in num_board.flatten():
        if n == -1:
            spaces += "0"
            symbols += "0"
        else:
            spaces += "1"
            symbols += str(n)
    bin_str = symbols + spaces
    return int(bin_str, 2)

def get_row_col_diags(
    board:np.ndarray, 
    row_idx:int, 
    col_idx:int, 
    directions:list=['row','col', 'diag', 'antidiag']
) -> dict:
    """ 
    Returns the row, col, diagonal and anti-diagonal 
    from a given position in the board.
    @param board: Game board (2D numpy array).
    @param row_idx: Index of row in the board.
    @param col_idx: Index of column in the board.
    @param directions: What directions are to be returned?
                       By, default, all directions are
                       returned.
    @return: A dictionary with values being a dictionary 
             that maps the 2 tuple position on the board
             to its content. The keys of the parent
             dictionary correspond to the row, column,
             diagonal and anti-diagonal that given row
             and column position falls within.
    """
    to_return = {}

    for direction in directions:
        if direction == 'row':
            to_return['row'] = {
                (row_idx, i): board[row_idx, i]
                for i in range(board.shape[1])
            }
        elif direction == 'col':
            to_return['col'] = {
                (i, col_idx): board[i, col_idx]
                for i in range(board.shape[0])
            }
        elif direction == 'diag':
            row_indices = range(
                max(0, row_idx - min(row_idx, col_idx)), 
                min(board.shape[0], row_idx + board.shape[1] - col_idx)
            )
            col_indices = range(
                max(0, col_idx - min(row_idx, col_idx)), 
                min(board.shape[1], col_idx + board.shape[0] - row_idx)
            )
            to_return['diag'] = {
                (row_indices[i], col_indices[i]): board[row_indices[i], col_indices[i]] 
                for i in range(min(len(row_indices), len(col_indices)))
            }
        else: # direction == 'antidiag'
            if not 'antidiag' in to_return:
                to_return['antidiag'] = {}
            i = row_idx
            j = col_idx
            while j >= 0 and i < board.shape[0]:
                to_return['antidiag'][(i, j)] = board[i, j]
                i += 1
                j -= 1

            i = row_idx-1 
            j = col_idx+1
            while i >= 0 and j < board.shape[1]:
                to_return['antidiag'][(i, j)] = board[i, j]
                i -= 1
                j += 1

            sorted_keys = sorted(to_return['antidiag'].keys())
            to_return['antidiag'] = {
                key: to_return['antidiag'][key] 
                for key in sorted_keys
            }
    return to_return

def int2board(board_int:int) -> np.ndarray:
    """ 
    Given a board as an 84 bit integer,
    as encoded using the board2int(...) 
    function, return the board as a 
    numpy array.
    @param board_int: Board from some player's 
                      perspective as an integer.
    @return: Board as an numpy array.
    """
    binary_str = bin(board_int)[2:].zfill(84)
    board = np.array([-1]*42)
    symbols = binary_str[:42]
    spaces = binary_str[42:]
    for i in range(42):
        if spaces[i] == '1':
            board[i] = int(symbols[i])
    board = board.reshape(6, 7)
    return board