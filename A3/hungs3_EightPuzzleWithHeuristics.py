'''
Stephen Hung, netid: hungs3
hungs3_EightPuzzleWithHeuristics.py
Eight Puzzle with Heuristic Functions.
 Version 0.4, January 25, 2018.


Usage:
  python3 AStar.py EightPuzzleWithHeuristics h_euclidean "[3, 1, 2, 4, 0, 5, 6, 7, 8]"

  AStar search for Eight Puzzle using the heuristic h_euclidian.
  The initial state for Eight Puzzle is the string list provided.

'''

import math

#<METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Eight Puzzle"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "8-JAN-2018"
PROBLEM_DESC=\
'''This formulation of the Eight Puzzle With Heuristics uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
class State:
  def __init__(self, b):
    if len(b)==9:
      list_of_lists = [b[:3],b[3:6],b[6:]]
    else:
      list_of_lists = b
    self.b = list_of_lists

  def __eq__(self,s2):
    for i in range(3):
      for j in range(3):
        if self.b[i][j] != s2.b[i][j]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    # Might not be needed in normal operation with GUIs.
    txt = "\n["
    for i in range(3):
      txt += str(self.b[i])+"\n "
    return txt[:-2]+"]"

  def __hash__(self):
    return (self.__str__()).__hash__()

  def h_euclidian(self):
    '''
      Compute the euclidean distance for each of the eight tiles from its location in the state to its location in the goal state. 
      Then it should add up these distances and return that sum. 
    '''
    distance_sum = 0
    goal_state_coords = [[0,1,2],[3,4,5],[6,7,8]]
    current_location = {}

    # Create a dictionary for where key = number and value = coordinates
    for row in range(3):
      for col in range(3):
        current_location[self.b[row][col]] = [row,col]

    # Compare coordinates with goal_state_coords
    for row in range(3):
      for col in range(3):
        a = goal_state_coords[row][col] # the number
        if(a != 0):
          a_coords = [row,col] # coords of the goal state of the number
          b = current_location[a] # current location of the number
          distance_sum += math.sqrt( (a_coords[0]-b[0])**2 + (a_coords[1] - b[1])**2 )
    return distance_sum

  def h_hamming(self):
    '''
      should determine the number of tiles that, in the state, are not where they should end up in the goal state. 
      (The maximum value of this heuristic is 8, in the case that none of the eight tiles is where it belongs.) 
    '''
    count = 0
    goal_state = [[0,1,2],[3,4,5],[6,7,8]]
    for i in range(3):
      for j in range(3):
        if(goal_state[i][j] != 0): # If it is a tile (not 0)
          if(goal_state[i][j] != self.b[i][j]): # If the goal state and current location is not the same.
            count+=1
    if(count > 8):
      raise Exception('Hamming Count should not be greater than 8')
    return count

  def h_manhattan(self):
    '''
      for each tile, how many rows it is away from its goal-state row 
      plus how many columns it is away from its goal-state column, 
      and it should add those distances for each of the tiles.
    '''
    distance = 0
    goal_state = [[0,1,2],[3,4,5],[6,7,8]]
    current_location = {}

    # Create a dictionary for where key = number and value = coordinates
    for row in range(3):
      for col in range(3):
        current_location[self.b[row][col]] = [row,col]

    # Go through every tile of the 3x3.
    for row in range(3):
      for col in range(3):
        if(goal_state[row][col] != 0): # If there is a tile. (not 0)
          # Manhattan Distance calculation
          goal_location = current_location[goal_state[row][col]]
          distance += abs(row - goal_location[0])
          distance += abs(col - goal_location[1])
    return distance

  def h_custom(self):
    '''
      Returns the average of the manhattan, hamming, and euclidian heuristic.
    '''
    # 0.1 because manhattan expands too many states normally ~1000
    # hamming works fine
    # Euclidian produces the best results *3 (*2 is only 10, 21, 20)
    return ( (self.h_manhattan()*0.1) + self.h_hamming() + (self.h_euclidian() * 2))/3

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    news.b = [row[:] for row in self.b]
    return news

  def find_void_location(self):
    '''Return the (vi, vj) coordinates of the void.
    vi is the row index of the void, and vj is its column index.'''
    for i in range(3):
      for j in range(3):
        if self.b[i][j]==0:
          return (i,j)
    raise Exception("No void location in state: "+str(self))

  def can_move(self,dir):
    '''Tests whether it's legal to move a tile that is next
       to the void in the direction given.'''
    (vi, vj) = self.find_void_location()
    if dir=='N': return vi<2
    if dir=='S': return vi>0
    if dir=='W': return vj<2
    if dir=='E': return vj>0
    raise Exception("Illegal direction in can_move: "+str(dir))

  def move(self,dir):
    '''Assuming it's legal to make the move, this computes
       the new state resulting from moving a tile in the
       given direction, into the void.'''
    news = self.copy() # start with a deep copy.
    (vi, vj) = self.find_void_location()
    b = news.b
    if dir=='N': 
      b[vi][vj] = b[vi+1][vj]
      b[vi+1][vj] = 0
    if dir=='S':
      b[vi][vj] = b[vi-1][vj]
      b[vi-1][vj] = 0
    if dir=='W':
      b[vi][vj] = b[vi][vj+1]
      b[vi][vj+1] = 0
    if dir=='E':
      b[vi][vj] = b[vi][vj-1]
      b[vi][vj-1] = 0
    return news # return new state

        
def goal_test(s):
  '''If all the b values are in order, then s is a goal state.'''
  return s == State([[0,1,2],[3,4,5],[6,7,8]])
  sdsdsds

def goal_message(s):
  return "You've got all eight straight. Great!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
  # Use default, but override if new value supplied
             # by the user on the command line.
CREATE_INITIAL_STATE = lambda: State(init_state_list)
#</INITIAL_STATE>

#<OPERATORS>
directions = ['N','E','W','S']
OPERATORS = [Operator("Move a tile "+str(dir)+" into the void",
                      lambda s,dir1=dir: s.can_move(dir1),
                      # The default value construct is needed
                      # here to capture the value of dir
                      # in each iteration of the list comp. iteration.
                      lambda s,dir1=dir: s.move(dir1) )
             for dir in directions]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<HEURISTIC>

#</HEURISTIC

