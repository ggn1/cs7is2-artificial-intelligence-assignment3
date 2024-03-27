### This file defines an agent that will learn
### to play the given game via tabular Q learning.

# Imports.
import random
import numpy as np
from typing import Callable

class TabQLearning:
    """ 
    An agent that learns to play the given game 
    via reinforcement learning, specifically 
    tabular Q learning.
    """

    def __init__(self, 
        discount_factor:float, 
        learning_rate:float, 
        r_tab:np.ndarray,
        is_game_over:Callable,
        get_next_states:Callable,
        get_next_state:Callable,
        change_threshold:float
    ):
        """
        Constructor.
        @param discount_factor: Factor by which rewards get 
                                discounted over time.
        @param learning_rate: Learning rate.
        @param change_threshold: Q table change threshold below which 
                                 algorithm is considered to have converged.
        @param r_tab: Reward(state, action) table.
        @param is_game_over: A function that returns true if a
                             given state is terminal or false
                             otherwise.
        @param get_next_states: A function that returns next states
                                reachable from any given state.
        @param get_next_state: A function that returns state arrived
                               at when given action a is executed from
                               given state s.
        """
        self.gamma = discount_factor
        self.alpha = learning_rate
        self.epsilon = change_threshold
        self.r_tab = r_tab
        self.is_game_over = is_game_over
        self.get_next_states = get_next_states
        self.get_next_state = get_next_state
        self.num_states = r_tab.shape[0]
        self.num_actions = r_tab.shape[1]
        self.q_tab = np.zeros((
            self.num_states, 
            self.num_actions
        )) # Q table is initialized with all 0s.

    def learn(self, max_episodes:int=-1):
        """ 
        Perform Q learning to determine best 
        Q table values that maximize rewards
        for this player.
        @param max_episodes: Maximum no. of episodes. Is -1 by 
                             default which indicates that the
                             algorithm may continue until convergence.
        """
        print('Learning ...')
        e = max_episodes # Keep track of no. of episodes left.
        q_diff = float('inf') # How different the q table is between 2 episodes.
        # 1. Loop for each episode until either
        #    the algorithm has converged (change in
        #    Q table values between 2 episodes < 
        #    change threshold) or the maximum allowed
        #    no. of episodes has been reached.
        while e != 0 or q_diff > self.epsilon: 
            # 2. Pick a random start state.
            s = random.randint(0, self.num_states-1) # inclusive
            # 3. Do while a terminal state has not yet been reached.
            while not self.is_game_over(s):
                # 4. From a list of possible actions from this 
                #    state s, pick a random one.
                possible_actions = self.get_next_states(s)
                a = possible_actions[random.randint(0, len(possible_actions)-1)]
                # 5. Compute Q and R value of executing action a in this state s.
                q_s_a = self.q_tab[s][a]
                r_s_a = self.r_tab[s][a]
                # 6. Get next state arrived at.
                sn = self.get_next_state(s, a)
                # 7. Get highest Q value among that of all
                #    (next state, possible next action) pairs.
                max_q_sn_an = float('-inf')
                for an in self.get_next_states(sn):
                    q_sn_an = self.q_tab[sn][an]
                    if q_sn_an > max_q_sn_an: 
                        max_q_sn_an = q_sn_an
                # 8. Compute the following formula and update Q value:
                #    Q(s, a) <-- (1 - alpha) Q(s, a) + alpha [
                #       R(s, a) + { gamma x max_an[ Q(sn, an) ] }
                #    ]
                self.q_tab[s][a] = (
                    ((1 - self.alpha) * q_s_a) + 
                    (self.alpha * (r_s_a + (self.gamma * max_q_sn_an)))
                )
                # 9. Set the next state to be the new current state.
                s = sn
            e -= 1 # Reduce no. of episodes left.
            print(f'Episode {e} done.')
        print('All done.')

    def get_move(self, s):
        """ 
        Based on given state and current
        Q table, returns the action that 
        maximizes the Q value.
        @param s: Given state from which a move
                  is to be made.
        @param return: Best move from given state.
        """
        return np.argmax(self.q_tab[s])