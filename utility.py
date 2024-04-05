### This file contains common functions that all files can use.
import time
import random
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
    world_view = np.array([
        [int_to_char[i] for i in row] 
        for row in num_board
    ])
    return world_view

def switch_player_perspective(board_num:np.ndarray) -> np.ndarray:
    """ 
    Switches the board from perspective of one player 
    to that of the opponent.
    """
    board_opp = board_num.copy()
    board_opp[board_opp == 1] = 2
    board_opp[board_opp == 0] = 1
    board_opp[board_opp == 2] = 0
    return board_opp

def switch_player_perspective_int(board_int:int, board_size:tuple) -> int:
    """ 
    Switches the board integer from the perspective 
    of one player to that of the opponent's.
    @param board_int: Game board as integer.
    @param board_size: Size of encoded board.
    @return: Switched board as an integer.
    """
    board = int2board(board_int, board_size)
    board[board == 1] = 2
    board[board == 0] = 1
    board[board == 2] = 0
    return board2int(board)

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

def board2int(num_board:np.ndarray) -> int:
    """
    Converts binary string into an integer.
    This is by first obtaining an 2*len(num_board.flatten()) 
    bit long bit string that's representative of the 
    game board and then converting this bit 
    string into a number. The the half of the bits 
    correspond to whether a piece at each position of 
    the 2D board flattened into a 1D list is a [1] piece 
    or a [0] piece with 1 => [1] and 0 => [0]. 
    The next half of the bits indicate whether the position 
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

def int2board(board_int:int, board_shape:tuple) -> np.ndarray:
    """ 
    Given a board as an 84 bit integer,
    as encoded using the board2int(...) 
    function, return the board as a 
    numpy array.
    @param board_int: Board from some player's 
                      perspective as an integer.
    @param board_shape: Shape of the board that's 
                        encoded in the given integer.
    @return: Board as an numpy array.
    """
    board_len = board_shape[0] * board_shape[1]
    binary_str = bin(board_int)[2:].zfill(board_len*2)
    board = np.array([-1]*board_len)
    symbols = binary_str[:board_len]
    spaces = binary_str[board_len:]
    for i in range(board_len):
        if spaces[i] == '1':
            board[i] = int(symbols[i])
    board = board.reshape(board_shape)
    return board

def get_random_free_pos(board:np.ndarray) -> tuple:
    """
    Given a board state, returns a random free
    position on the board.
    @param state: Current state of the game board.
    @return: A random position on the game board that
                is free. Returns (-1, -1) if no free spaces.
    """
    empty_spots = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == -1:
                empty_spots.append((i, j))
    if len(empty_spots) <= 0:
        return (-1, -1)
    return random.choice(empty_spots)

def compute_sbsa(
    num_board: np.ndarray, 
    row_idx:int, 
    col_idx:int,
    directions:list,
    is_adjacent_playable_free:Callable=None
):
    """ 
    Returns what the maximum no. of side by side
    occurrences of each symbol (0/1) in the set of
    values extending out towards either side 
    in the given direction or directions from
    given position is.
    @param num_board: Board with numbers from a player's perspective.
    @param row_idx: Row index.
    @param col_idx: Column index.
    @param directions: Directions.
    @param is_adjacent_playable_free: A function that returns
                                        if a position adjacent to
                                        this one is free or not.
    @return: A dictionary that maps each given direction
            to a dictionary that maps no. of times in a 
            row with a list containing 3 tuples of the 
            form (start position, end position, SBSA) of 
            elements that meet the streak condition. Here the
            last element in the tuple is optional.
    """
    directional_board_values = get_row_col_diags(num_board, row_idx, col_idx, directions)
    sbsa_0 = {direction:{} for direction in directions}
    sbsa_1 = {direction:{} for direction in directions}
    # min_pos, max_pos, streak, has playable adjacent position
    for direction in directions:
        board_vals = directional_board_values[direction]
        streak_0 = [(-1, -1), (-1, -1), 0, False]  
        streak_1 = [(-1, -1), (-1, -1), 0, False]
        reset_0 = False
        reset_1 = False
        for pos, val in board_vals.items():
            if val == 0: 
                if streak_0[2] == 0:
                    streak_0[0] = pos
                streak_0[2] += 1
                streak_0[1] = pos
                reset_1 = True
            elif val == 1:
                if streak_1[2] == 0:
                    streak_1[0] = pos
                streak_1[2] += 1
                streak_1[1] = pos
                reset_0 = True
            else: # val == -1
                if not reset_0: reset_0 = True
                if not reset_1: reset_1 = True
            if reset_1:
                if streak_1[2] >= 2:
                    if not streak_1[2] in sbsa_1[direction]:
                        sbsa_1[direction][streak_1[2]] = [(
                            streak_1[0], streak_1[1],
                            is_adjacent_playable_free(
                                num_board, 
                                streak_1[0], 
                                streak_1[1],
                                direction=direction
                            )
                        )]
                    else:
                        sbsa_1[direction][streak_1[2]].append((
                            streak_1[0], streak_1[1],
                            is_adjacent_playable_free(
                                num_board, 
                                streak_1[0], 
                                streak_1[1],
                                direction=direction
                            )
                        ))
                streak_1 = [(-1, -1), (-1, -1), 0, False]
                reset_1 = False
            if reset_0:
                if streak_0[2] >= 2:
                    if not streak_0[2] in sbsa_0[direction]:
                        sbsa_0[direction][streak_0[2]] = [(
                            streak_0[0], streak_0[1],
                            is_adjacent_playable_free(
                                num_board, 
                                streak_0[0], 
                                streak_0[1],
                                direction=direction
                            )
                        )]
                    else:
                        sbsa_0[direction][streak_0[2]].append((
                            streak_0[0], streak_0[1],
                            is_adjacent_playable_free(
                                num_board, 
                                streak_0[0], 
                                streak_0[1],
                                direction=direction
                            )
                        ))
                streak_0 = [(-1, -1), (-1, -1), 0, False]
                reset_0 = False  
        if streak_1[2] >= 2:
            if not streak_1[2] in sbsa_1[direction]:
                sbsa_1[direction][streak_1[2]] = [(
                    streak_1[0], streak_1[1],
                    is_adjacent_playable_free(
                        num_board, 
                        streak_1[0], 
                        streak_1[1],
                        direction=direction
                    )
                )]
            else:
                sbsa_1[direction][streak_1[2]].append((
                    streak_1[0], streak_1[1],
                    is_adjacent_playable_free(
                        num_board, 
                        streak_1[0], 
                        streak_1[1],
                        direction=direction
                    )
                ))
        if streak_0[2] >= 2:
            if not streak_0[2] in sbsa_0[direction]:
                sbsa_0[direction][streak_0[2]] = [(
                    streak_0[0], streak_0[1],
                    is_adjacent_playable_free(
                        num_board, 
                        streak_0[0], 
                        streak_0[1],
                        direction=direction
                    )
                )]
            else:
                sbsa_0[direction][streak_0[2]].append((
                    streak_0[0], streak_0[1],
                    is_adjacent_playable_free(
                        num_board, 
                        streak_0[0], 
                        streak_0[1],
                        direction=direction
                    )
                ))
    return sbsa_0, sbsa_1