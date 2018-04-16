'''
hungs3_Farmer_Fox_etc.py
by Stephen Hung

Assignment 2, in CSE 415, Winter 2018.

This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.

Problem Description:
There is a Farmer, Fox, Chicken, and Grain on the left bank of a river.
The farmer has a boat to can carry the farmer and item across the river.
The farmer wants to carry all of his items to the right bank of the river.
However, the Fox can't be left with the Chicken and the Chicken can't be left
with the Grain.
Figure out how to carry everything to the right bank of the river.
'''

#<METADATA>
SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['S. Hung']
PROBLEM_CREATION_DATE = "15-JAN-2018"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
'''
There is a Farmer, Fox, Chicken, and Grain on the left bank of a river.
The farmer has a boat to can carry the farmer and item across the river.
The farmer wants to carry all of his items to the right bank of the river.
However, the Fox can't be left with the Chicken and the Chicken can't be left
with the Grain.
Figure out how to carry everything to the right bank of the river.
'''

#</METADATA>


#<COMMON_DATA>
#</COMMON_DATA>


#<COMMON_CODE>
FARMER=0  # array index to access farmer counts
FOX=1  # same idea for fox
CHICKEN=2 # same idea for chicken
GRAIN=3 # same idea for grain
LEFT=0 # same idea for left side of river (2D array - first row)
RIGHT=1 # same idea for right side of river (2D array - second row)

class State():
    def __init__(self, d=None):
        # Initialize the state.
        if d==None:
            d = {'items':[[0,0],[0,0],[0,0],[0,0]],
                'boat': LEFT}
        self.d = d

    def __eq__(self,s2):
        # Find out if the States are equal.
        for prop in ['items', 'boat']:
          if self.d[prop] != s2.d[prop]: 
            return False
        return True

    def __str__(self):
    # Produces a textual description of a state.
        p = self.d['items']
        txt = "\n Farmer on left:"+str(p[FARMER][LEFT])+"\n"
        txt += "   Fox on left:"+str(p[FOX][LEFT])+"\n"
        txt += "   Chicken on left:"+str(p[CHICKEN][LEFT])+"\n"
        txt += "   Grain on left:"+str(p[GRAIN][LEFT])+"\n"
        txt += " Farmer on right:"+str(p[FARMER][RIGHT])+"\n"
        txt += "   Fox on right:"+str(p[FOX][RIGHT])+"\n"
        txt += "   Chicken on right:"+str(p[CHICKEN][RIGHT])+"\n"
        txt += "   Grain on right:"+str(p[GRAIN][RIGHT])+"\n"
        side='left'
        if self.d['boat']==RIGHT: 
            side='right'
            txt += " boat is on the "+side+".\n"
        return txt

    def __hash__(self):
        # Hash the State (for hash tables)
        return (self.__str__()).__hash__()

    def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
        news = State({})
        news.d['items']=[self.d['items'][M_or_C][:] for M_or_C in [FARMER, FOX, CHICKEN, GRAIN]]
        news.d['boat'] = self.d['boat']
        return news 

    def can_move(self,farm,f,c,g):
        '''Tests whether it's legal to move the boat and take
         f foxes c chickens, and g grains.'''
        side = self.d['boat'] # Where the boat is.
        p = self.d['items']
        # Farmer is not on the same side as the boat - noone to row the boat.
        if(p[FARMER][side] == 0): return False 

        fox_available = p[FOX][side]
        if fox_available < f: return False # Can't take more foxes than available

        chicken_available = p[CHICKEN][side]
        if chicken_available < c: return False # Can't take more chickens than available

        grain_available = p[GRAIN][side]
        if grain_available < g: return False # Can't take more grain than available

        if(f==1): 
            # If fox is moved, will it be left with the chicken, is the fox away from the grain, and is the farmer not with the fox
            if(p[FOX][1-LEFT] == p[CHICKEN][LEFT] 
                and p[FOX][1-LEFT] != p[GRAIN][LEFT] 
                and p[FARMER][LEFT] == p[FOX][1-LEFT]):
                return False
            if(p[CHICKEN][LEFT] == p[GRAIN][LEFT] 
                and p[CHICKEN][LEFT] != p[FOX][1-LEFT] 
                and p[FARMER][LEFT] == p[CHICKEN][LEFT]):
                return False
        elif(c==1): # If chicken is moved, will it be left with the fox or grain and the farmer isn't with them.
            if(p[FOX][LEFT] == p[CHICKEN][1-LEFT] 
                and p[FOX][LEFT] != p[GRAIN][LEFT] 
                and p[FOX][LEFT] == p[FARMER][LEFT]):
                return False
            if(p[CHICKEN][1-LEFT] == p[GRAIN][LEFT] 
                and p[CHICKEN][1-LEFT] != p[FOX][LEFT] 
                and p[CHICKEN][1-LEFT] == p[FARMER][LEFT]):
                return False
        elif(g==1): # If grain is moved, will it be left with the chicken and the farmer or fox isn't with them.
            if(p[CHICKEN][LEFT] == p[GRAIN][1-LEFT] 
                and p[CHICKEN][LEFT] != p[FOX][LEFT] 
                and p[CHICKEN][LEFT] == p[FARMER][LEFT]):
                return False
            if(p[FOX][LEFT] == p[CHICKEN][LEFT] 
                and p[FOX][LEFT] != p[GRAIN][1-LEFT] 
                and p[FOX][LEFT] == p[FARMER][LEFT]):
                return False

        return True

    def move(self,farm,f,c,g):
        '''Assuming it's legal to make the move, this computes
         the new state resulting from moving the boat carrying
         the farmer and f foxes, c chickens, and g grains'''
        news = self.copy()      # start with a deep copy.
        side = self.d['boat']         # where is the boat?
        p = news.d['items']          # get the array of arrays of people.
        p[FARMER][side] = p[FARMER][side]-farm     # Remove farmer from the current side.
        p[FOX][side] = p[FOX][side]-f     # Remove fox from the current side.
        p[CHICKEN][side] = p[CHICKEN][side]-c     # Remove chicken from the current side.
        p[GRAIN][side] = p[GRAIN][side]-g     # Remove grain from the current side.
        p[FARMER][1-side] = p[FARMER][1-side]+farm # Add farmer at the other side.
        p[FOX][1-side] = p[FOX][1-side]+f # Add Fox to other side
        p[CHICKEN][1-side] = p[CHICKEN][1-side]+c # Add Chicken to the other side.
        p[GRAIN][1-side] = p[GRAIN][1-side]+g # Add Grain to other side
        news.d['boat'] = 1-side       # Move the boat itself.
        return news

def goal_test(s):
    '''If all items are on the right, then s is a goal state.'''
    p = s.d['items']
    return (p[FOX][RIGHT]==1 and p[CHICKEN][RIGHT]==1 and p[GRAIN][RIGHT]==1 and p[FARMER][RIGHT]==1)

def goal_message(s):
  return "Congratulations on successfully guiding the farmer and his fox, chicken, and grain across the river!"

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
CREATE_INITIAL_STATE = lambda : State(d={'items':[[1,0],[1,0],[1,0],[1,0]],'boat':LEFT})
#</INITIAL_STATE>


#<OPERATORS>
MC_combinations = [(1,0,0,0),
                    (1,1,0,0),
                    (1,0,1,0),
                    (1,0,0,1)]

OPERATORS = [Operator(
  "Cross the river with "+str(farm)+" Farmers, "+str(f)+" fox, "+str(c)+" chicken, and "+str(g)+" grain",
  lambda s, farm1=farm, f1=f, c1=c, g1=g: s.can_move(farm1,f1,c1,g1),
  lambda s, farm1=farm, f1=f, c1=c, g1=g: s.move(farm1,f1,c1,g1) ) 
  for (farm,f,c,g) in MC_combinations]
#</OPERATORS>


#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

