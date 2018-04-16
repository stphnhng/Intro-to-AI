''' 
Stephen Hung, netid: hungs3
hungs3_BreadthFS.py
Breadth First Search of a problem space.
 Version 0.4, January 20, 2018.

 Usage:
 python3 hungs3_BreadthFS.py TowersOfHanoi
  The numbered STEP comments in the function BreadthFS correspond
 to the algorithm steps for breadth first search as presented
 in Slide 8 of the "Basic Search Algorithms" lecture.
'''

import sys

if sys.argv==[''] or len(sys.argv)<2:
#  import TowersOfHanoi as Problem
  import TowersOfHanoi as Problem
else:
  import importlib
  # Import User entered Problem as Problem
  Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to hungs3_BreadthFS")
COUNT = None
BACKLINKS = {}

'''
  This function runs the Breadth First Search and creates the Initial State
'''
def runBFS():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH
  COUNT = 0
  BACKLINKS = {}
  MAX_OPEN_LENGTH = 0
  BreadthFS(initial_state)
  print(str(COUNT)+" states expanded.")
  print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))

''' 
This functions performs iterative Breadth First Search
Parameters:
  inital_state: this is the starting state from which BFS starts with.
'''
def BreadthFS(initial_state):
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH

# STEP 1. Put the start state on a list OPEN
  OPEN = [initial_state]
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
    S = OPEN.pop(0)
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
    for op in Problem.OPERATORS:
      if op.precond(S):
        new_state = op.state_transf(S)
        if not (new_state in CLOSED):
          L.append(new_state)

# STEP 5. Delete from L any members of OPEN that occur on L.
#         Insert all members of L at the back of OPEN.
    for s2 in OPEN:
      for i in range(len(L)):
        if (L[i] == s2):
          del L[i]; break

    for i in L:
      BACKLINKS[i] = S
    OPEN = OPEN + L # Adds L to the end of OPEN
    print_state_list("OPEN", OPEN)
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
  runBFS()

