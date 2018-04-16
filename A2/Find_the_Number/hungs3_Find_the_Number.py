'''
hungs3_Find_the_Number.py
by Stephen Hung

Assignment 2, in CSE 415, Winter 2018.

This file contains my problem formulation for the "Find The Number" Problem.

Problem Description:
The user will input two parameters to this program.
The first is a random number to be guessed and the second is the 
maximum number that is guessable.
The user will guess the random number through a series of questions 
instead of directly guessing it.
The user will be provided with the numbers that could be the random number.
For the random number (n), provided integer (k), and provided integer (m),
the user will ask if n-k is divisible by m by providing the k and m.
This will narrow down the possibilities and once the only possibility is the random number
the user will have won.
'''

#<METADATA>
SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "Find The Number"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['S. Hung']
PROBLEM_CREATION_DATE = "17-JAN-2018"


PROBLEM_DESC=\
'''
The user will input two parameters to this program.
The first is a random number to be guessed and the second is the 
maximum number that is guessable.
The user will guess the random number through a series of questions 
instead of directly guessing it.
The user will be provided with the numbers that could be the random number.
For the random number (n), provided integer (k), and provided integer (m),
the user will ask if n-k is divisible by m by providing the k and m.
This will narrow down the possibilities and once the only possibility is the random number
the user will have won.
'''
#</METADATA>


#<COMMONDATA>

randomInt = 0 # Mystery Number
MAX_NUMBER = 10 # Max Number

try:
    import sys
    randomInt = int(sys.argv[2]) # User's input for random integer
    MAX_NUMBER = int(sys.argv[3]) # User's input for maximum possible number
except:
    print('Please input a random integer and the max, e.g. integer of 2 and max of 10:')
    print('python ../Int_Solv_Client.py hungs3_Find_the_Number 2 10')
    raise Exception('Did not enter a 3rd or 4th parameter')

#</COMMONDATA>


#<COMMONCODE>
import math

'''
This function checks if 'm' is a prime.
Parameters:
  m: the number to be checked
Returns:
  True/False: If the number is a prime.
'''
def isPrime(m):
    if(m <= 1):
        return False
    for i in range(2,m):
        if(m % i == 0):
            return False    
    return True


'''
This function checks if 0 <= k < m and if m is prime
Furthermore, it checks if (n-k) is divisible by m.
Parameters:
  n: The randomly generated integer to be guessed
  k: The integer to be subtracted from n.
  m: The integer to check (n-k)'s divisibility.
Returns:
  True/False: If (n-k) is divisible by m and if 0 <= k < m 
              and m is a prime.
'''
def is_n_minus_k_divisible_by_m(n,k,m):
    if(k < 0 or m <= k):
        return False

    if(not isPrime(m)):
        return False

    if( (n-k) % m != 0):
        return False

    return True

class State():
    def __init__(self, d=None):
        # Initialize the State
        if(d==None):
            d={'possibilities': [0],
                'phase': 0, 
                'lastm': -1}
        self.d = d

    def __eq__(self, s2):
        # Check if the States are equal to each other.
        for x in ['possibilities', 'phase']:
          if self.d[x] != s2.d[x]: 
            return False
        return True

    def __str__(self):
        # Returns the string representation of the State.
        txt = "question_phase: "+str(self.d['phase'])+"\n"
        if(self.d['lastm'] == -1):
            txt += "last_m: None\n"
        else:
            txt += "last_m: "+str(self.d['lastm'])+"\n"
        txt += "possibilities: "+str(self.d['possibilities'])+"\n"
        return txt


    def __hash__(self):
        # Hash the State (for hash tables)
        return (self.__str__()).__hash__()

    def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
        news = State({})
        news.d['possibilities'] = [i for i in self.d['possibilities']]
        news.d['phase'] = self.d['phase']
        news.d['lastm'] = self.d['lastm']
        return news 

    def divis_can_move(self,p):
        # Determines if a number is a prime and the phase is for division.
        if(not isPrime(p) or self.d['phase'] != 0):
            return False
        return True

    def sub_can_move(self,p):
        # Determines if a number is < the prime previously chosen (m) and 
        # the phase is subtraction.
        if(p >= int(self.d['lastm']) or self.d['phase'] != 1):
            return False

        return True


    def move(self, p):
        # "Moves" by removing the possibilities that do not follow the question.

        news = self.copy()
        new_possibilities = []
        if(news.d['phase'] == 0):
            # Divisiblity phase
            news.d['lastm'] = p
            news.d['phase'] = 1
        elif(news.d['phase'] == 1): 
            # Subtraction phase
            followsCondition = False
            if(is_n_minus_k_divisible_by_m(randomInt,p,news.d['lastm'])):
                # If (random number - k) is divisible by m, then remove all numbers that aren't.
                followsCondition = True
            else:
                # If it isn't, remove all numbers that are
                followsCondition = False

            for i in news.d['possibilities']:
                # For all current numbers in the possibilities
                if(followsCondition and is_n_minus_k_divisible_by_m(i, p, news.d['lastm'])):
                    # add all numbers that are divisible to the possiblities
                    new_possibilities.append(i)
                elif(not followsCondition and not is_n_minus_k_divisible_by_m(i, p, news.d['lastm'])):
                    # add all numbers that are not divisble to the possiblities
                    new_possibilities.append(i)
            news.d['phase'] = 0 # Switch phase to division.
            news.d['possibilities'] = new_possibilities
        return news



def goal_test(s):
    '''If the number has been guessed, then s is the goal state.'''
    p = s.d['possibilities']
    return (p[0]==randomInt)

def goal_message(s):
  return "Congratulations on successfully guessing the number!"


class Operator():
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)
#</COMMONCODE>


#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'possibilities':[i for i in range(MAX_NUMBER+1)],'phase':0,'lastm': -1})
#</INITIAL_STATE>


#<OPERATORS>

number_range = [i for i in range(MAX_NUMBER+1)]
# range(MAX_NUMBER+1) in order to get 0 to MAX_NUMBER

prime_range = []
# Range of prime numbers from 2 to the MAX_NUMBER + 1
for i in range(MAX_NUMBER+1):
    if(isPrime(i)):
        prime_range.append(i)


# Operators for division.
PHASE_1_OPERATORS = [Operator(
  "Is N divisible by "+str(p)+ " after ...",
  lambda s, p1=p: s.divis_can_move(p1),
  lambda s, p1=p: s.move(p1) ) 
  for (p) in prime_range]

# Operators for subtraction.
PHASE_2_OPERATORS = [Operator(
  "... subtracting "+str(p) + " ?",
  lambda s, p1=p: s.sub_can_move(p1),
  lambda s, p1=p: s.move(p1) ) 
  for (p) in number_range]

# Combine the operators.
OPERATORS = PHASE_1_OPERATORS + PHASE_2_OPERATORS
#</OPERATORS>


#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>




