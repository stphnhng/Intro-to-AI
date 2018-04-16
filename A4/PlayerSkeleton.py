'''PlayerSkeleton.py
A bare-bones agent that plays Toro-Tile Straight,
but rather poorly.

To create your own agent, make a copy of this file, using
the naming convention YourUWNetID_TTS_agent.py.

If you need to import additional custom modules, use
a similar naming convention... e.g.,
YourUWNetID_TTS_custom_static.py


'''

from TTS_State import TTS_State

USE_CUSTOM_STATIC_EVAL_FUNCTION = False

class MY_TTS_State(TTS_State):
  def static_eval(self):
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      return self.custom_static_eval()
    else:
      return self.basic_static_eval()

  def basic_static_eval(self):
    raise Exception("basic_static_eval not yet implemented.")

  def custom_static_eval(self):
    raise Exception("custom_static_eval not yet implemented.")


def take_turn(current_state, last_utterance, time_limit):

    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = MY_TTS_State(current_state.board)
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'  
    if who=='B': new_who = 'W'  
    new_state.whose_turn = new_who
    
    # Place a new tile
    location = _find_next_vacancy(new_state.board)
    if location==False: return [[False, current_state], "I don't have any moves!"]
    new_state.board[location[0]][location[1]] = who

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    move = location

    # Make up a new remark
    new_utterance = "I'll think harder in some future game. Here's my move"

    return [[move, new_state], new_utterance]

def _find_next_vacancy(b):
    for i in range(len(b)):
      for j in range(len(b[0])):
        if b[i][j]==' ': return (i,j)
    return False

def moniker():
    return "Buddy" # Return your agent's short nickname here.

def who_am_i():
    return """My name is (WHATEVER YOU DECIDE AS YOUR AGENT's NAME), created by (YOUR NAME).
(MORE INFO, SUCH AS:) I consider myself to be an aggressive line-blocker."""

def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like setting up Zobrist hashing, here.
    return "OK"

# The following is a skeleton for the function called tryout,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player
# and then it will be able to call tryout using something like this:
# tryout_results = player.tryout(**kwargs)

def tryout(
       game_initial_state=None,
       current_state=None,
       max_ply=2,
       use_iterative_deepening = False,
       use_row_major_move_ordering = False,
       alpha_beta=False, 
       timed=False, 
       time_limit=1.0,
       use_zobrist=False,
       use_custom_static_eval_function=False):

  # All students, add code to replace these default
  # values with correct values from your agent (either here or below).
  current_state_dynamic_val = -1000.0
  current_state_static_val  = -1000.0
  n_states_expanded = 0
  n_static_evals_performed = 0
  max_depth_reached = 0

  # Those students doing the optional alpha-beta implementation,
  # return the correct number of cutoffs from your agent (either here or below).
  n_ab_cutoffs = 0

  # For those of you doing Zobrist hashing, have your
  # agent determine these values and include the correct
  # values here or overwrite the default values below.
  n_zh_put_operations = 0
  n_zh_get_operations = 0
  n_zh_successful_gets = 0
  n_zh_unsuccessful_gets = 0
  zh_hash_value_of_current_state = 0

  # STUDENTS: You may create the rest of the body of this function here.

  # Prepare to return the results...
  results = []
  results.append(current_state_dynamic_val)
  results.append(current_state_static_val)
  results.append(n_states_expanded)
  results.append(n_static_evals_performed)
  results.append(max_depth_reached)
  results.append(n_ab_cutoffs)
  results.append(n_zh_put_operations)
  results.append(n_zh_get_operations)
  results.append(n_zh_successful_gets)
  results.append(n_zh_unsuccessful_gets)
  results.append(zh_hash_value_of_current_state)
  # Actually return the list of all results...
  return(results)

