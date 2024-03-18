'''Farmer_Fox.py
[STUDENTS: REPLACE THE FOLLOWING INFORMATION WITH YOUR
OWN:]
by Nur Ahmed
UWNetIDs: nurrr
Student numbers: 2266025

Assignment 2, in CSE 415, Winter 2024
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name(s), uwnetid(s), and 7-digit student number(s) are given above in 
# the format shown.

# You should model your code closely after the given example problem
# formulation in HumansRobotsFerry.py

# Put your metadata here, in the same format as in HumansRobotsFerry.
#<METADATA>
SOLUTION_VERSION = "1.0"
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['N. Ahmed']
PROBLEM_CREATION_DATE = "20-JAN-2024"

# Start your Common Code section here.
#<COMMON_CODE>
FARMER = 0  # array index to access the farmer
F = 1  # array index to access the fox
C = 2  # array index to access the chicken
G = 3  # array index to access the grain
LEFT = 0  # array index for left side
RIGHT = 1  # array index for right side

class State:

    # include methods similar to those in HumansRobotsFerry.py for
    # this class.
    def __init__(self, d=None):
        if d is None:
            d = {'items': [0,0,0,0], 'boat': LEFT}
        self.d = d

    def __eq__(self, s2):
        for prop in ['items', 'boat']:
            if self.d[prop] != s2.d[prop]: return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        items = self.d['items']
        txt = "Farmer on left" if items[FARMER] == LEFT else "Farmer on right"
        txt += ", Fox on left" if items[F] == LEFT else ", Fox on right"
        txt += ", Chicken on left" if items[C] == LEFT else ", Chicken on right"
        txt += ", Grain on left" if items[G] == LEFT else ", Grain on right"
        txt += ", Boat on left" if self.d['boat'] == LEFT else ", Boat on right"
        return txt

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        return State({'items': self.d['items'][:], 'boat': self.d['boat']})

    def can_move(self, item):
        side = self.d['boat']  # Where the boat (and the farmer) is.
        
        # The farmer must always be able to move
        if self.d['items'][FARMER] != side:
            return False

        # If moving an item other than the farmer, check if it's on the same side
        if item != FARMER and self.d['items'][item] != side:
            return False

        new_side = 1 - side
        new_items = self.d['items'][:]
        new_items[FARMER] = new_side  # Farmer always moves
        if item != FARMER: 
            new_items[item] = new_side  # Move the specified item

        # Check for invalid states after the move
        # Conditions where the farmer is not present to supervise
        if new_items[F] == new_items[C] and new_items[F] != new_side:
            return False
        if new_items[C] == new_items[G] and new_items[C] != new_side:
            return False

        return True

    def move(self, item):
        news = self.copy()
        side = self.d['boat']

        # Move the farmer and the specified item
        news.d['items'][FARMER] = 1 - side  # Farmer always moves
        if item != FARMER:  # Move the specified item if it's not the farmer
            news.d['items'][item] = 1 - side

        # Move the boat
        news.d['boat'] = 1 - side
        return news

def goal_test(self):
    return all(self.d['items'][i] == RIGHT for i in range(4))

def goal_message(s):
    return "Congratulations on successfully getting the Farmer, Fox, Chicken, and Grain across!"



# Put your INITIAL STATE section here.

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda: State(d={'items': [0, 0, 0, 0], 'boat': LEFT})
#</INITIAL_STATE>


# Put your OPERATORS section here.

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

#<OPERATORS>
FCG_combinations = [(1, 0, 0, 0), (1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1)]

OPERATORS = [Operator("Move Farmer alone", 
             lambda s: s.can_move(FARMER),
             lambda s: s.move(FARMER)),
    Operator("Move Farmer with Fox", 
             lambda s: s.can_move(F),
             lambda s: s.move(F)),
    Operator("Move Farmer with Chicken", 
             lambda s: s.can_move(C),
             lambda s: s.move(C)),
    Operator("Move Farmer with Grain", 
             lambda s: s.can_move(G),
             lambda s: s.move(G))]
#<OPERATORS>

# Finish off with the GOAL_TEST and GOAL_MESSAGE_FUNCTION here.

#<GOAL_TEST> 
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> 
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

