'''
hungs3_TTS_agent.py
Stephen Hung
2/2/18

A bare-bones agent that plays Toro-Tile Straight,
but rather poorly.

To create your own agent, make a copy of this file, using
the naming convention YourUWNetID_TTS_agent.py.

If you need to import additional custom modules, use
a similar naming convention... e.g.,
YourUWNetID_TTS_custom_static.py


'''
import time
from TTS_State import TTS_State

USE_CUSTOM_STATIC_EVAL_FUNCTION = False
INITIAL_BOARD = None
OPPONENT_MONIKER = None
SIDE = None
K = None
MAXPLY = 2
STARTTIME = None
TIMELIMIT = 0
TIME_BOOL = True
UTTERANCES = ["I'm the best!", 
                "Dang, even I surprise myself!", 
                "Take a look at this gorgeous move!",
                "My brilliance is as bright as the sun... no wait, its even better",
                "Do you even know who I am?",
                "Even Stephen Curry bows before me... or was that Stephen Hawking",
                "gg ez",`
                "See if you can beat this",
                "You underestimated me, now reap your consequences",
                "Don't act like you're not impressed"]
TURNCOUNT = 0
STATIC_EVAL_PERFORMED = 0
MAX_DEPTH = 0
USE_IDDFS = True

class MY_TTS_State(TTS_State):

    def static_eval(self):
        global STATIC_EVAL_PERFORMED
        STATIC_EVAL_PERFORMED+=1

        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    '''
    This function checks each tile's 4 directions (NE, N, NW, and W) to see
    if it contains a row of K tiles with inARow # of letters and nothing else.
    parameters:
        letter: the letter we are looking for (either 'W' or 'B')
        inARow: the number of letters in a row we are looking for (with nothing else in the row)
    '''
    def performRowChecks(self, letter, inARow):
        global K # The K
        notLetter = other(letter)
        wRowWorksSum = 0 # number of rows fulfilling the condition of inARow letters and nothing else
        for row in range(len(self.board)): #index for row
            for col in range(len(self.board[row])): #index for col
                # Check North
                letterSumInRow = 0
                notLetterSumInRow = 0
                blankSumInRow = 0
                blockSumInRow = 0
                for i in range(K):
                    xCoord = row-i
                    yCoord = col
                    if(row - i < 0): # Checks if it needs to loop around the board
                        tile = str(self.board[len(self.board)-i+row][col])
                    else:
                        tile = str(self.board[xCoord][yCoord])
                    if tile == letter:
                        letterSumInRow+=1
                    elif tile == notLetter:
                        notLetterSumInRow+=1
                    elif tile == '-':
                        blockSumInRow+=1
                if(letterSumInRow == inARow and notLetterSumInRow == 0 and blockSumInRow == 0):
                    # inARow letters, no other letters or blocks
                    wRowWorksSum+=1
                # Check North East
                letterSumInRow = 0
                notLetterSumInRow = 0
                blankSumInRow = 0
                blockSumInRow = 0
                for i in range(K):
                    # If the board needs to loop around
                    if(row - i < 0 and col+i >= len(self.board[row])):
                        tile = str(self.board[len(self.board)-i+row][abs(len(self.board[row])-i-col)])
                    elif(row - i < 0):
                        tile = str(self.board[len(self.board)-i+row][col-i])
                    elif(col+i >= len(self.board[row])):
                        tile = str(self.board[row-i][abs(len(self.board[row])-i-col)])
                    else:
                        tile = str(self.board[row-i][col+i])
                    if tile == letter:
                        letterSumInRow+=1
                    elif tile == notLetter:
                        notLetterSumInRow+=1
                    elif tile == '-':
                        blockSumInRow+=1
                if(letterSumInRow == inARow and notLetterSumInRow == 0 and blockSumInRow == 0):
                    # inARow letters, no other letters or blocks
                    wRowWorksSum+=1
                # Check North West
                letterSumInRow = 0
                notLetterSumInRow = 0
                blankSumInRow = 0
                blockSumInRow = 0
                for i in range(K):
                    # if needs to loop around the board
                    if(row - i < 0 and col-i < 0):
                        tile = str(self.board[len(self.board)-i+row][len(self.board[row])-i+col])
                    elif(row - i < 0):
                        tile = str(self.board[len(self.board)-i+row][col-i])
                    elif(col - i < 0):
                        tile = str(self.board[row-i][len(self.board[row])-i+col])
                    else:
                        tile = str(self.board[row-i][col-i])
                    if tile == letter:
                        letterSumInRow+=1
                    elif tile == notLetter:
                        notLetterSumInRow+=1
                    elif tile == '-':
                        blockSumInRow+=1
                if(letterSumInRow == inARow and notLetterSumInRow == 0 and blockSumInRow == 0):
                    # inARow letters, no other letters or blocks
                    wRowWorksSum+=1
                # Check West
                letterSumInRow = 0
                notLetterSumInRow = 0
                blankSumInRow = 0
                blockSumInRow = 0
                for i in range(K):
                    # if it needs to loop around the board
                    if(col - i < 0):
                        tile = str(self.board[row][len(self.board[row]) - i+col])
                    else:
                        tile = str(self.board[row][col-i])
                    if tile == letter:
                        letterSumInRow+=1
                    elif tile == notLetter:
                        notLetterSumInRow+=1
                    elif tile == '-':
                        blockSumInRow+=1
                if(letterSumInRow == inARow and notLetterSumInRow == 0 and blockSumInRow == 0):
                    # inARow letters, no other letters or blocks
                    wRowWorksSum+=1
        return wRowWorksSum

    '''
    This function does a basic static evaluation of the state's current board
    It finds all rows in the board with 2 W's in a row and everything else vacant
    and does the same for B.
    Then it subtracts count of W - count of B and returns that count
    '''
    def basic_static_eval(self):
        global K
        sumCount = 0
        # Checks rows for 2 'W's in a row and nothing else
        wCount = self.performRowChecks('W',2)
        # Checks rows for 2 'B's in a row and nothing else
        bCount = self.performRowChecks('B',2)
        sumCount = wCount - bCount
        return sumCount

    '''
    This function does a custom static evaluation of the current state's board
    It uses the equation from lecture slides:
        h(s) = 100 A + 10 B + C – (100 D + 10 E + F)
        A = number of lines of 3 Ws in a row.
        B = number of lines of 2 Ws in a row (not blocked by an B)
        C = number of lines containing one W and no Bs.
        D = number of lines of 3 Bs in a row.
        E = number of lines of 2 Bs in a row (not blocked by an W)
        F = number of lines containing one B and no Ws.

    '''
    def custom_static_eval(self):
        # tic tac toe one in 07 slides?

        A = self.performRowChecks('W',3)
        B = self.performRowChecks('W',2)
        C = self.performRowChecks('W',1)

        D = self.performRowChecks('B',3)
        E = self.performRowChecks('B',2)
        F = self.performRowChecks('B',1)

        formula = (100*A) + (10*B) + (C) - ( (100*D) + (10*E) + F )
        return formula


'''
Takes a turn according to what best locations are found through static evaluation of all positions on the board
The best position is found via min-max search.
'''
def take_turn(current_state, last_utterance, time_limit):
    global TURNCOUNT, UTTERANCES
    TURNCOUNT +=1
    if(TURNCOUNT == 10):
        TURNCOUNT = 0
    global STARTTIME, TIMELIMIT
    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = current_state
    new_state.__class__ = MY_TTS_State
    new_state.static_eval() # For static eval testing purposes only
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'  
    if who=='B': new_who = 'W'  
    new_state.whose_turn = new_who
    
    if USE_IDDFS:
        # DO IDDFS w/ depth going into minimax
        if TIME_BOOL:
            TIMELIMIT = time_limit
        STARTTIME = time.time() # Timer to time the time used while finding best location.
        iterNum = MAXPLY # max ply depth being searched
        for i in range(iterNum+1):
            # +1 cause 0 is not usable as a ply
            minimaxResult = minimax(new_state, SIDE, i+1)
            if(str(type(minimaxResult)) != '<class \'int\'>'): # ply = 0, minimax returns an int
                bestValue, bestLocation = minimaxResult
            else:
                bestLocation = _find_next_vacancy(new_state.board)
                if bestLocation==False: return [[False, current_state], "I don't have any moves!"]
    else:
        bestLocation = _find_next_vacancy(new_state.board)
        if bestLocation==False: return [[False, current_state], "I don't have any moves!"]

    # Place a new tile

    new_state.board[bestLocation[0]][bestLocation[1]] = who

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    #move = location
    move = bestLocation

    # Make up a new remark (Cocky attitude)

    new_utterance = UTTERANCES[TURNCOUNT]

    return [[move, new_state], new_utterance]

# Returns the other player given the current player
def other(letter):
    if(letter == 'W'):
        return 'B'
    return 'W'

# Returns all successor states given the current board + turn
def successors(state, whosTurn):
    board = state.board
    successorBoards = []
    for i in range(len(board)):
      for j in range(len(board[i])):
        if board[i][j]==' ': 
            new_state = state.copy()
            new_board = new_state.board
            new_board[i][j] = whosTurn
            new_state.__class__ = MY_TTS_State
            successorBoards.append((new_state,(i,j)))
    return successorBoards

# ply = depth (# of turns you are looking ahead)
'''
    Performs a minimax search using the current state
    Param:
        state is the current MY_TTS_State
        whosTurn is a character ('W' or 'B') representing whos turn it is
        ply is the current depth of the minimax search.
'''
def minimax(state, whosTurn, ply):
    global MAX_DEPTH
    if(ply > MAX_DEPTH):
        MAX_DEPTH = ply
    if ply == 0:
        return state.static_eval()
    if(time.time() >= STARTTIME + TIMELIMIT - 0.1) and TIME_BOOL:
        return state.static_eval()
    if(successors(state,whosTurn) == []):
        return 100000
    if whosTurn == 'W': #Maximinizing W's win rate
        provisional = -100000
    else:
        provisional = 100000
    returnState = None
    returnCoords = None

    for loc in successors(state, whosTurn):
        # iterates through all successors and finds the best static eval value for W
        s = loc[0]
        coords = loc[1]
        newVal = minimax(s, other(whosTurn), ply-1)
        if(str(type(newVal))) == '<class \'tuple\'>' :
            newVal = newVal[0]
        if(whosTurn == 'W' and newVal > provisional) or (whosTurn == 'B' and newVal < provisional):
            provisional = newVal
            returnCoords = coords
            returnState = s
    return (provisional,returnCoords)

def _find_next_vacancy(b):
    for i in range(len(b)):
      for j in range(len(b[0])):
        if b[i][j]==' ': return (i,j)
    return False

def moniker():
    return "TTSPRO" # Return your agent's short nickname here.

def who_am_i():
    return """My name is TTS Pro, created by Stephen Hung (hungs3). I consider myself to be an depressive line-blocker."""

'''
    Initializes global constant values according to the parameters.
'''
def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like setting up Zobrist hashing, here.
    global K, SIDE, OPPONENT_MONIKER
    initial_state.__class__ = MY_TTS_State
    INITIAL_BOARD = initial_state
    K = k
    SIDE = who_i_play
    OPPONENT_MONIKER = player2Nickname
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

    global MAXPLY, USE_CUSTOM_STATIC_EVAL_FUNCTION, STATIC_EVAL_PERFORMED, USE_IDDFS, TIMELIMIT, TIME_BOOL, MAX_DEPTH


    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    current_state_dynamic_val = -1000.0
    if(current_state != None):
        current_state.__class__ = MY_TTS_State
        current_state_static_val  = current_state.static_eval()
    else:
        current_state_static_val = -1000.0
    n_states_expanded = 0
    n_static_evals_performed = STATIC_EVAL_PERFORMED
    max_depth_reached = MAX_DEPTH

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
    MAXPLY = max_ply
    USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function
    USE_IDDFS = use_iterative_deepening
    TIMELIMIT = time_limit
    TIME_BOOL = timed

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

