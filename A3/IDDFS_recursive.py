''' hungs3_IDDFS.py
Iterative-Deepening Depth-First Search of a problem space.
 Version 0.4, January 22, 2018.
 Stephen Hung

 Usage:
 python3 hungs3_IDDFS.py TowersOfHanoi
  The numbered STEP comments in the function Iterative-Deepening Depth-First Search correspond
 to the algorithm steps for iterative-deepening depth-first as presented
 in Slide 8 of the "Basic Search Algorithms" lecture.
'''

import sys

if sys.argv==[''] or len(sys.argv)<2:
#  import EightPuzzle as Problem
  import TowersOfHanoi as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to ItrDFS")
COUNT = None
BACKLINKS = {}

def runIDDFS():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH, DEPTH
  COUNT = 0
  BACKLINKS = {}
  MAX_OPEN_LENGTH = 0
  DEPTH = 0 # Limiting Depth
  goal_reached = False

  for d in range(5):  
    print('--------')
    print('new max depth:'+str(DEPTH))
    print('--------')
    OPEN = [initial_state]
    CLOSED = []
    BACKLINKS[initial_state] = None
    for i in range(0,DEPTH):
      print('current depth usage: ' + str(i))
      found = IterativeDDFS(OPEN, CLOSED, i)
      if(found):
        quit()
    DEPTH+=1
  print(str(COUNT)+" states expanded.")
  print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))

def IterativeDDFS(OPEN, CLOSED, depth):
  global COUNT, MAX_OPEN_LENGTH, BACKLINKS, DEPTH
  if(depth <= DEPTH):
    if depth == 0 and len(OPEN) == 1:
      if Problem.GOAL_TEST(OPEN[0]):
        print(Problem.GOAL_MESSAGE_FUNCTION(S))
        path = backtrace(S)
        print('Length of solution path found: '+str(len(path)-1)+' edges')
        return True
    if depth > 0 and OPEN != []:
      print()
      report(OPEN,CLOSED,COUNT)
      if len(OPEN) > MAX_OPEN_LENGTH: 
        MAX_OPEN_LENGTH = len(OPEN)
      S = OPEN.pop(0)
      CLOSED.append(S)

      if(Problem.GOAL_TEST(S)):
        print(Problem.GOAL_MESSAGE_FUNCTION(S))
        path = backtrace(S)
        print('Length of solution path found: '+str(len(path)-1)+' edges')
        return True
      COUNT += 1

      L = []
      print('parent = ' + str(S))
      if(depth != DEPTH):
        for op in Problem.OPERATORS:
          if op.precond(S):
            new_state = op.state_transf(S)
            if not(new_state in CLOSED):
              L.append(new_state)
              if(new_state not in BACKLINKS):
                BACKLINKS[new_state] = S

      for s2 in OPEN:
        for i in range(len(L)):
          if (L[i] == s2):
            del L[i]; break

      if(L != []):
        print_state_list("children = ", L)
      else:
        print('children = ' + str(L))
      OPEN = L + OPEN
      if(OPEN != []):
        print_state_list("OPEN", OPEN)
      else:
        print('OPEN = ' + str(OPEN))
      if(depth+1 > DEPTH and OPEN != []):
        return IterativeDDFS(OPEN,CLOSED,depth)
      else:
        return IterativeDDFS(OPEN, CLOSED, depth+1)
  return False


def print_state_list(name, lst):
  print(name+" is now: ",end='')
  for s in lst[:-1]:
    print(str(s),end=', ')
  print(str(lst[-1]))

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
  
def report(open, closed, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("len(CLOSED)="+str(len(closed)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
  runIDDFS()

