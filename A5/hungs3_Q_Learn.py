'''hungs3_Q_Learn.py

Rename this file using your own UWNetID, and rename it where it is imported
in TOH_MDP.py
Implement Q-Learning in this file by completing the implementations
of the functions whose stubs are present.
Add or change code wherever you see #*** ADD OR CHANGE CODE HERE ***

This is part of the UW Intro to AI Starter Code for Reinforcement Learning.

'''

import random

# Edit the returned name to ensure you get credit for the assignment.
def student_name():
#*** ADD OR CHANGE CODE HERE ***
   return "Hung, Stephen" # For an autograder.

STATES=None; ACTIONS=None; UQV_callback=None; Q_VALUES=None
is_valid_goal_state=None; Terminal_state = None
USE_EXPLORATION_FUNCTION = None
INITIAL_STATE = None
def setup(states, actions, q_vals_dict, update_q_value_callback,\
    goal_test, terminal, use_exp_fn=False):
    '''This method is called by the GUI the first time a Q_Learning
    menu item is selected. It may be called again after the user has
    restarted from the File menu.
    Q_VALUES starts out with all Q-values at 0.0 and a separate key
    for each (s, a) pair.'''
    global STATES, ACTIONS, UQV_callback, Q_VALUES, is_valid_goal_state
    global USE_EXPLORATION_FUNCTION, Terminal_state
    STATES = states
    ACTIONS = actions
    Q_VALUES = q_vals_dict
    UQV_callback = update_q_value_callback
    is_valid_goal_state = goal_test
    Terminal_state = terminal
    USE_EXPLORATION_FUNCTION = use_exp_fn
    if USE_EXPLORATION_FUNCTION:
#*** ADD OR CHANGE CODE HERE ***
         # Change this if you implement an exploration function:
         print("You have not implemented an exploration function")

PREVIOUS_STATE = None
LAST_ACTION = None
def set_starting_state(s):
    '''This is called by the GUI when a new episode starts.
    Do not change this function.'''
    global INITIAL_STATE, PREVIOUS_STATE
    print("In Q_Learn, setting the starting state to "+str(s))
    INITIAL_STATE = s
    PREVIOUS_STATE = s

ALPHA = 0.5
CUSTOM_ALPHA = False
EPSILON = 0.5
CUSTOM_EPSILON = False
GAMMA = 0.9

def set_learning_parameters(alpha, epsilon, gamma):
    ''' Called by the system. Do not change this function.'''
    global ALPHA, EPSILON, CUSTOM_ALPHA, CUSTOM_EPSILON, GAMMA
    ALPHA = alpha
    EPSILON = epsilon
    GAMMA = gamma
    if alpha < 0: CUSTOM_ALPHA = True
    else: CUSTOM_ALPHA = False
    if epsilon < 0: CUSTOM_EPSILON = True
    else: CUSTOM_EPSILON = False

def update_Q_value(previous_state, previous_action, new_value):
    '''Whenever your code changes a value in Q_VALUES, it should
    also call this method, so the changes can be reflected in the
    display.
    Do not change this function.'''
    UQV_callback(previous_state, previous_action, new_value)

def handle_transition(action, new_state, r):
    '''When the user drives the agent, the system will call this function,
    so that you can handle the learning that should take place on this
    transition.'''
    global PREVIOUS_STATE, ALPHA, GAMMA

#*** ADD OR CHANGE CODE HERE ***
    
    # You should call update_Q_value before returning.  E.g.,
    if not Q_VALUES:
        for a in ACTIONS:
            Q_VALUES[(new_state,a)] = 0

    max_sample = 0
    for act in ACTIONS:
        if(is_valid_goal_state(new_state)):
            sample = r + GAMMA * Q_VALUES[(new_state, "Exit")]
        elif(act == 'Exit'):
            sample = -float('inf')
        sample = r + GAMMA * Q_VALUES[(new_state,act)]
        max_sample = max(max_sample, sample)
    Q_VALUES[(PREVIOUS_STATE, action)] = ((1-ALPHA) * Q_VALUES[(PREVIOUS_STATE,action)]) + (ALPHA * max_sample)
    update_Q_value(PREVIOUS_STATE, action, Q_VALUES[(PREVIOUS_STATE, action)])
    if CUSTOM_ALPHA:
        ALPHA *= 0.98

    PREVIOUS_STATE = new_state
    return # Nothing needs to be returned.

def choose_next_action(s, r, terminated=False):
    '''When the GUI or engine calls this, the agent is now in state s,
    and it receives reward r.
    If terminated==True, it's the end of the episode, and this method
    can just return None after you have handled the transition.

    Use this information to update the q-value for the previous state
    and action pair.

    Then the agent needs to choose its action and return that.

    '''
    global INITIAL_STATE, PREVIOUS_STATE, LAST_ACTION, ALPHA
    # ALPHA is a global val for the alpha value.
    # Unless s is the initial state, compute a new q-value for the
    # previous state and action.
    if not s == INITIAL_STATE:
        if not Q_VALUES:
            for a in ACTIONS:
                Q_VALUES[(s,a)] = 0

        max_sample = 0 # max sample for use in Q value formula.
        for act in ACTIONS:
            if(is_valid_goal_state(s)): # if it is the goal state, only compute the exit sample score. 
                sample = r + GAMMA * Q_VALUES[(s, "Exit")]
            elif(act == 'Exit'):
                sample = -float('inf') # if the action is exit and its not the goal state, then make sure its not chosen.
            sample = r + GAMMA * Q_VALUES[(s,act)]
            max_sample = max(max_sample, sample)
        Q_VALUES[(PREVIOUS_STATE, LAST_ACTION)] = ((1-ALPHA) * Q_VALUES[(PREVIOUS_STATE, LAST_ACTION)]) + (ALPHA * max_sample)
        update_Q_value(PREVIOUS_STATE, LAST_ACTION, Q_VALUES[(PREVIOUS_STATE, LAST_ACTION)])
        # update q values.

        if USE_EXPLORATION_FUNCTION:
            print("You have not implemented an exploration function")
    #*** ADD OR CHANGE CODE HERE ***

#*** ADD OR CHANGE CODE HERE ***
    if CUSTOM_ALPHA: # if there is a custom alpha, change alpha by factor of 98%
        ALPHA = ALPHA * 0.98
    max_q_value = 0
    max_action = ACTIONS[0]
    LAST_ACTION = max_action # remember this for next time
    PREVIOUS_STATE = s        #    "       "    "   "    "
    if is_valid_goal_state(s):
        # if its goal state, exit.
        LAST_ACTION = "Exit"
        return "Exit"
    elif s == Terminal_state or terminated:
        # if its terminating, return None
        return None
    else:
        # find the max action which corresponds to the max Q value.
        max_val = 0
        for a in ACTIONS:
            temp_q_value = Q_VALUES[(s, a)]
            if(temp_q_value > max_val):
                max_val = temp_q_value
                max_action = a
        max_action = epsilon_greedy_func(max_action) # use epsilon greedy algorithm
        LAST_ACTION = max_action
        return max_action 

'''
    This function returns either a random action or the chosen action based on the epsilon form.
    param:
        current_action is the current chosen action based on Q Learning
'''
def epsilon_greedy_func(current_action):
    global EPSILON
    epsi = EPSILON
    randNum = random.random()
    if(randNum <= epsi):
        randActNum = random.randint(0,6)
        return ACTIONS[randActNum]
    else:
        return current_action

Policy = {}
def extract_policy(S, A):
    '''Return a dictionary mapping states to actions. Obtain the policy
    using the q-values most recently computed.  If none have yet been
    computed, call return_Q_values to initialize q-values, and then
    extract a policy.
    Ties between actions having the same (s, a) value can be broken arbitrarily.
    Reminder: goal states should map to the Exit action, and no other states
    should map to the Exit action.
    '''
    global Policy
    Policy = {}
    if not Policy:
        for s in S:
            for a in A:
                Policy[s] = a
   
#*** ADD OR CHANGE CODE HERE ***
    for s in S:
        cur_q_value = 0
# for state s in state list S
        for a in A:
            if(Q_VALUES[(s,a)] > cur_q_value):
                cur_q_value = Q_VALUES[(s,a)]
                Policy[s] = a
    return Policy
