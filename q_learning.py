### This file defines the tabular Q learning strategy.

# Imports.
import os
import json
import random
import numpy as np
from strategies import Strategy
from utility import track_time
from utility import print_debug
from typing import Callable, Tuple
from utility import get_opposite_symbol

class TabQLearning(Strategy):
    """ 
    An agent that learns to play the given game 
    via reinforcement learning, specifically 
    tabular Q learning.
    """

    def __init__(self, 
        get_reward:np.ndarray,
        is_game_over:Callable,
        get_next_states:Callable,
        get_next_state:Callable,
        states:list,
        actions:list
    ):
        """
        Constructor.
        @param r_tab: Reward(state, action) table.
        @param is_game_over: A function that returns true if a
                             given state is terminal or false
                             otherwise.
        @param get_next_states: A function that returns next states
                                reachable from any given state.
        @param get_next_state: A function that returns state arrived
                               at when given action a is executed from
                               given state s.
        @param states: List of all possible states.
        @param actions: List of all possible actions.
        """
        self.name = 'TabQLearning'
        self.r_tab = r_tab
        self.is_game_over = is_game_over
        self.get_next_states = get_next_states
        self.get_next_state = get_next_state
        self.states = states
        self.actions = actions
        self.q_tab = np.full((
            len(self.states), 
            len(self.actions)
        ), -100) # Q table is initialized with all -infinity.

    def __choice_count_check(self, 
        choice_counts:dict,
        state_count:int, 
        picked_count:int
    ):
        """ Checks if given no. of states have been chosen as 
            start state during learning at least given 
            no. of times.
            @param choice_count: Mapping of state index to no. of 
                                 times chosen as starting state.
            @param state_count: No. of states that are to have 
                                been picked at least picked_count
                                no. of times.
            @param picked_count: No. of times state_count no. of 
                                 states must have at least been
                                 picked as start state for.
            @return: True if condition is met and false otherwise.
        """
        num_states_true = 0
        for c in choice_counts.values():
            if c >= picked_count:
                num_states_true += 1
        return num_states_true >= state_count

    def __is_stopping_condition_met(self,
        num_episodes_left:int,
        q_diff:int,
        change_threshold:int,
        start_choice_threshold:dict,
        choice_counts:dict
    ): 
        """
        Checks if a stopping condition for learning has been met.
        @param num_episodes_left: Maximum no, of episodes allowed.
        @param q_diff: Current max difference in Q table between episodes.
        @param change_threshold: Min Q table change needed.
        @param start_choice_threshold: No. of times some states have to be 
                                       chosen as start state.
        @param choice_counts: No. of times states were chosen so far
                              as start state.
        """
        is_max_episodes_reached = num_episodes_left == 0 
        if is_max_episodes_reached:
            print(f"Max episodes reached.")
            return True
        is_change_threshold_met = q_diff <= change_threshold 
        is_start_choice_threshold_met = (
            start_choice_threshold is not None and 
            self.__choice_count_check(
                choice_counts=choice_counts,
                state_count=start_choice_threshold['state_count'],
                picked_count=start_choice_threshold['choice_count']
            )
        )
        if is_start_choice_threshold_met:
            print(f"Start state choice count met.")
            return True
        if is_change_threshold_met:
            print(f"Q Table difference change threshold met.")
            return True
        return False

    def learn(self, 
        symbols:Tuple[str, str], 
        max_episodes:int,
        discount_factor:float, # gamma
        learning_rate:float, # alpha
        change_threshold:int=-1, # epsilon,
        start_choice_threshold=None
    ):
        """ 
        Perform Q learning to determine best 
        Q table values that maximize rewards
        for this player.
        @param discount_factor: Factor by which rewards get 
                                discounted over time.
        @param learning_rate: Learning rate.
        @param symbols: Symbols associated with each player.
        @param change_threshold: A value for average difference between
                                 Q tables from 2 different episodes 
                                 which being reached => stop learning.
        @param max_episodes: Maximum no. of episodes. Is -1 by 
                             default which indicates that the
                             algorithm may continue until convergence.
        @param start_choice_threshold: Defines the no. of states that have
                                       to be chosen as start states at
                                       least given no. of times before 
                                       which learning may be stopped.
                                       Expected format = {
                                            "state_count": <int>,
                                            "choice_count": <int>
                                       }
        """
        print('Learning ...')
        e = max_episodes # Keep track of no. of episodes left.
        q_diff = float('inf') # How different the q table is between 2 episodes.
        max_states_visited = 0 # The maximum no. of states that
                               # were visited in any episode.
        num_episodes = 0 # Episode counter.
        start_states = self.states.copy() # A list of starting states to choose from.
        choice_counts = {i:0 for i in range(len(self.states))}
        try:
            # 1. Loop for each episode until either
            #    the algorithm has converged (change in
            #    Q table values between 2 episodes < 
            #    change threshold) or the maximum allowed
            #    no. of episodes has been reached.
            while not self.__is_stopping_condition_met(
                num_episodes_left = e,
                q_diff = q_diff,
                change_threshold = change_threshold,
                start_choice_threshold = start_choice_threshold,
                choice_counts = choice_counts
            ):
                num_episodes += 1

                # Q table from last episode
                # saved so that difference after
                # this episode may be calculated
                # at the end of this episode.
                if change_threshold >= 0:
                    q_tab_freeze = self.q_tab.copy() 

                # 2. Pick a random start state.
                #    Never picks same state again 
                #    in the same episode.
                if len(start_states) == 0: 
                    # The start states array is to 
                    # ensure more states get visited
                    # in the random process.
                    start_states = self.states.copy()
                i = random.randint(0, len(start_states)-1) # inclusive
                s = start_states.pop(i) 
                s_idx = self.states.index(s)
                choice_counts[s_idx] += 1

                # 3. Do while a terminal state has not yet been reached.
                num_states_visited = 0 # No. of states visited.
                while not self.is_game_over(s):
                    # 4. From the list of possible actions from this 
                    #    state s, pick a random one.
                    possible_state_actions = (
                        self.get_next_states(state=s, sym=symbols[0])
                        + self.get_next_states(state=s, sym=symbols[1])
                    )
                    j = random.randint(0, len(possible_state_actions)-1)
                    sn, a = possible_state_actions.pop(j)
                    a_idx = self.actions.index(a) # Random action from s.
                    
                    # 5. Get next state arrived at
                    #    by executing randomly selected
                    #    action a from state s.
                    sn_idx = self.states.index(sn)
                    
                    # 6. Get highest Q value among that of all
                    #    (next state, possible next action) pairs.
                    max_q_sn_an = float('-inf')
                    for an_idx in range(self.q_tab.shape[1]):
                        q_sn_an = self.q_tab[sn_idx][an_idx]
                        if q_sn_an > max_q_sn_an: 
                            max_q_sn_an = q_sn_an

                    # 7. Compute the following formula and update Q value:
                    #    Q(s, a) <-- (1 - alpha) Q(s, a) + alpha [
                    #       R(s, a) + { gamma x max_an[ Q(sn, an) ] }
                    #    ]
                    q_s_a = self.q_tab[s_idx][a_idx]
                    r_s_a = self.r_tab[s_idx][a_idx]
                    self.q_tab[s_idx][a_idx] = (
                        ((1 - learning_rate) * q_s_a) + 
                        (learning_rate * (r_s_a + (discount_factor * max_q_sn_an)))
                    )
                    # 8. Set the next state to be the new current state.
                    s = sn
                    
                    # Update performance metric.
                    num_states_visited += 1
                    max_states_visited = max(
                        num_states_visited, 
                        max_states_visited
                    )

                # Reduce no. of episodes left.
                if e != -1:
                    e -= 1

                # Update q_diff.
                if change_threshold >= 0:
                    q_diff = np.max(np.abs(self.q_tab - q_tab_freeze))

            print(f'All done. Episodes = {num_episodes}.')
        except KeyboardInterrupt:
            return ('Keyboard Interrupt', max_states_visited)

    def load_qtab(self, src:str):
        """ 
        Load a previously learned Q table
        stored as a json file.
        """
        if not ".json" in src:
            raise Exception(f"File src must be a .json file.")
        
        with open(src, 'r') as f:
            self.q_tab = np.array(json.load(f))
        
        print(f"Loaded Q table from {src}.")

    def save_qtab(self, name:str, folder:str='.'):
        """ 
        Function saves the Q table so that
        training need not be done every time
        from scratch.
        @param folder: Folder at which to save file.
        @param name: Name of file.
        """
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        dst = f"{folder}/{name}.json"
        with open(dst, 'w') as f:
            json.dump(self.q_tab.tolist(), f)

        print(f"Saved Q table at {dst}.")

    @track_time
    def get_move(self, state:Tuple, sym:str) -> int:
        """ 
        Based on given state and current
        Q table, returns the action that 
        maximizes the Q value.
        @param state: Given state from which a move
                      is to be made.
        @param sym: This player's symbol.
        @param return: Index of the action to take.
        """
        s_idx = self.states.index(state)
        # Get indices actions that this player can take.
        a_idx_player = [
            a_idx for a_idx in range(len(self.actions)) 
            if sym == self.actions[a_idx][2]
        ]
        # Get index of action corresponding to
        # the highest Q value from given state
        # for given player.
        q_max = float('-inf')
        a_idx_best = -1
        for a_idx in a_idx_player:
            q = self.q_tab[s_idx, a_idx]
            if q > q_max:
                q_max = q
                a_idx_best = a_idx
        # Return index of best action.
        return a_idx_best