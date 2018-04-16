''' 
Stephen Hung, netid: hungs3
hungs3_AStar.py
AStar Search of a problem space.
 Version 0.4, January 22, 2018.
 Stephen Hung, Univ. of Washington.

 Usage:
  python3 hungs3_AStar.py EightPuzzleWithHeuristics h_euclidean "[3, 1, 2, 4, 0, 5, 6, 7, 8]"

  AStar search for Eight Puzzle using the heuristic h_euclidian.
  The initial state for Eight Puzzle is the string list provided.
'''

import sys
import importlib
import re

from priorityQB import PriorityQB
Problem_Initial_State = None # Inital State of the Problem
INITIAL_STATE_INPUTTED = None # User Inputed inital state

if sys.argv==[''] or len(sys.argv)<4:
  import hungs3_EightPuzzleWithHeuristics as Problem # Default Problem is Eight Puzzle
  Heuristic = 'h_euclidian' # Default Heuristic is h_euclidian
  INITIAL_STATE_INPUTTED = [3, 1, 2, 4, 0, 5, 6, 7, 8] # Default Inital State
else:
  Problem = importlib.import_module(sys.argv[1]) # Custom Problem
  Heuristic = sys.argv[2] # Custom Heuristic
  INITIAL_STATE_INPUTTED = list(map(int,re.findall('[0-9]', sys.argv[3])))
  # Regex expression to take in custom initial state


print("\nWelcome to hungs3_AStar")
COUNT = None
BACKLINKS = {}

'''
  This function runs the AStar Search and creates the inital state.
'''
def runAStar():
  initial_state = Problem.State(INITIAL_STATE_INPUTTED) 
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH
  COUNT = 0
  BACKLINKS = {}
  MAX_OPEN_LENGTH = 0
  AStarSearch(initial_state)
  print(str(COUNT)+" states expanded.")
  print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))

'''
  Implements the AStar Search by including the heuristic value of the state in the calculation:
  f = g + h where f is priority, g is the # of nodes from start, and h is the heuristic value.
  Parameters:
    initial_state is the state that the problem starts with.
'''
def AStarSearch(initial_state):
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH

# STEP 1. Put the start state on a list OPEN
  OPEN = PriorityQB()
  OPEN_STATES = [] # List of OPEN States for usage when printing (printing tuple in Priority Queue is hard)
  OPEN_STATES.append(initial_state)
  OPEN.insert((initial_state,0),0) # Inserts tuple (state, distance from start node) and the priority
  CLOSED = []
  BACKLINKS[initial_state] = None

# STEP 2. If OPEN is empty, output “DONE” and stop.
  while OPEN != []:
    report(OPEN, CLOSED, COUNT)
    if len(OPEN)>MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)

# STEP 3. Select the first state on OPEN and call it S.
#         Delete S from OPEN.
#         Put S on CLOSED.
#         If S is a goal state, output its description
    top_state = OPEN.deletemin()
    OPEN_STATES.pop(0)
    S = top_state[0][0] # State to be checked
    g = top_state[0][1] # distance from start node
    top_state_prio = top_state[1] # priority of current state
    CLOSED.append(S)


    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      path = backtrace(S)
      print('Length of solution path found: '+str(len(path)-1)+' edges')
      return
    COUNT += 1

# STEP 4. Generate the list L of successors of S and delete 
#         from L those states already appearing on CLOSED.
    L = []
    L_STATES = []
    for op in Problem.OPERATORS:
      if op.precond(S):
        new_state = op.state_transf(S)
        if new_state not in CLOSED:
          L.append((new_state,g+1)) # adds as tuple to make adding to OPEN easier.
          L_STATES.append(new_state)
          BACKLINKS[new_state] = S

# STEP 5. Delete from OPEN any members of OPEN that occur on L.
#         Insert all members of L at the front of OPEN.
    for s2 in L:
      for i in range(len(OPEN)):
        if s2 in OPEN:
          OPEN.remove(s2); break

    for s2 in L_STATES:
      for i in range(len(OPEN_STATES)):
        if s2 in OPEN_STATES:
          del OPEN_STATES[i]; break

    OPEN_STATES = L_STATES + OPEN_STATES

    for i in L:
      # Iterates through all L
      l_state = i[0] # children state
      g_num = i[1] # distance from start node to the children node
      h_value = getattr(l_state,Heuristic) # Calls the heuristic function from the children state
      f = h_value() + g_num
      OPEN.insert((i[0],i[1]),f)
    print_state_list("OPEN", OPEN_STATES) # print the open states (no priority)
# STEP 6. Go to Step 2.

'''
  This function is a custom print function for State Objects. 
  Parameters:
    name is the name of the list being printed.
    lst is the list to print.
'''
def print_state_list(name, lst):
  print(name+" is now: ",end='')
  for s in lst[:-1]:
    print(str(s),end=', ')
  print(str(lst[-1]))

'''
  This function backtraces the state S by seeing which state S is a child of.
  This is done by using the global var BACKLINKS
  Parameters:
    S is the state to be backtraced.
'''
def backtrace(S):
  global BACKLINKS
  path = []
  while S:
    path.append(S)
    S = BACKLINKS[S]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(s)
  return path    
  
'''
  This function reports the length of OPEN, length of CLOSED, 
  and the number of states expanded so far.
'''
def report(open, closed, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("len(CLOSED)="+str(len(closed)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
  runAStar()
