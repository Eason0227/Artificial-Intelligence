# water jug Solver Version 1. 31/3/2017 
# by Dr Loke K.S.

import itertools
import sys, random
from abc import ABCMeta, abstractmethod
import queue as Q
import pdb  #python debugger
#################
# Globals     ###
start=  [24, 0, 0, 0]  #fixed starting position
MAX = [24,13,11,5]
named={'A':0,'B':1,'C':2,'D':3} # provides index to the named containers
NA,NB,NC,ND=MAX
#NA = 24  # maximum of ounces hold in vase
#NB = 13  # maximum of ounces hold in vessel 1
#NC = 11  # maximum of ounces hold in vessel 2
#ND = 5   # maximum of ounces hold in vessel 3

#################

#
# Basic data structure Stack
#
#
class Stack:
     def __init__(self):
         self.items = []
     def isEmpty(self):
         return self.items == []
     def push(self, item):
         self.items.append(item)
     def pop(self):
         if(not self.isEmpty()):
              return self.items.pop()
     def peek(self):
         return self.items[len(self.items)-1]
     def size(self):
         return len(self.items)
#
# Basic data structure Queue
# (Use my own Queue instead of import) 
#        
class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def add(self, item):
        self.items.insert(0,item)
    def get(self):
        if(not self.isEmpty()):
             return self.items.pop()
    def size(self):
        return len(self.items)


#
# Solver Class: propose moves to the state Class 
#
#
class Solver(metaclass=ABCMeta):
    """
     ABC=Abstract base class
     Abstract Solver class that searches through the state space, called by the state class
    """
    @abstractmethod
    def get(self):
         raise NotImplementedError()
    @abstractmethod
    def add(self):
         raise NotImplementedError()

# Uses Breadth-first search		 
class BFS(Solver):
    """
     Concrete solver: must implement abstract methods from abstract class Solver
     uses a Queue
    """
    def __init__(self):
        self.queue=Queue()
    def get(self):
        return self.queue.get()
    def add(self,state):
        self.queue.add(state)

# Uses Depth-first search		
class DFS(Solver):
    """
     Concrete solver: must implement abstract methods from abstract class Solver
     Uses a Stack
    """
    def __init__(self):
        self.stack=Stack()
    def get(self):
        return self.stack.pop()
    def add(self,state):
        self.stack.push(state)

# Uses Heuristic search		
class Solver3(Solver):
    """
     Concrete solver 3: must implement abstract methods from abstract class Solver
     Uses the Python built-in Priority Queue
    """

    def __init__(self, goal):
        self.pq=Q.PriorityQueue() #get the smallest cost
        self.goal=goal
    def get(self):
        if not self.pq.empty():
             (val,state)=self.pq.get()
             return state
        else:
             return None
    def add(self, state):
        value=self.heuristic(state)
        self.pq.put((value,state))
        
    def heuristic(self,state):
        count=0;
        for x in range(4):
            if self.goal[x] != state[x]:
                count+=1
        return count
     
#  Game Class (Model): keep track on the abstract game state data. No animation or drawing
#                       methods. 
#

class Game:
    """Model class for the game that stores states about the game state.
       This class also include all the necessary operators.
       Does not handle Animation or screen processses.
    """
    
   
    def __init__(self):
        self.initialstate = start
        self.goal = [8,8,8,0]
        
        
        #### CHANGE THE SOLVER METHOD HERE ##
        #self.Solver=BFS() #Breath-first search
        #self.Solver=DFS() #Depth-first search
        self.Solver=Solver3(self.goal) #Heuristic search
        #####################################
               
    def solve(self): 
        #get state
        #get valid moves
        #put new state state in a data structure
        #repeat
        
        
        self.used=[]
        self.Solver.add(self.initialstate)
        state=self.Solver.get()
        #pdb.set_trace()

        found=False
        while not(found or (state is None)):
            moves=self.getMoves(state)
            #print("moves=",moves)
            for move in moves:
                #print("--->trying ...",move)
                temp=self.makeMove(state,move)
                self.used.append(state)                
                if not (temp in self.used):
                     self.printstate(temp,"--->moved ")
                     self.Solver.add(temp)
                     
                     if (temp==self.goal):
                          print("Found answer")
                          found=True
                          break
            state=self.Solver.get()
 
    def printstate(self, state, msg=None):
        print(msg, state)
        return
    
    
    def makeMove(self,state, move):
        """make a valid move and update the state """
        # This function does not check if the move is valid.
        A, B, C, D = state
        
        #Get the values of the From and To containers
        From=state[named[move[0]]]
        To=state[named[move[1]]]
        Pour = MAX[named[move[1]]] - To # Pour till filled unless From has less
        Pour = From if (From<Pour) else Pour

        #Update the state now as a new object
        state1=state[:]
        state1[named[move[0]]]=state[named[move[0]]]-Pour
        state1[named[move[1]]]=state[named[move[1]]]+Pour
        
        return state1
            
    
    def isValidMove(self, state, move):
        A, B, C, D = state

        # move e.g. = ('A','D') means pour from A to D
        # valid if condition is meet
        # 1. From (move[0]) is not empty
        # 2. To (move[1]) is not filled
        
        From=state[named[move[0]]]
        To=state[named[move[1]]]
        Max_To=MAX[named[move[1]]]
        
        #Valid to pour as long as there is empty space in To and From is not empty
        Pour = abs(From - Max_To - To) if From >0 else 0

        if(From > 0 and (Max_To-To)>0 and Pour>0):
             return True
        else:
             return False
        
        
    
    def getMoves(self,state, lastMove=None):
        """get all possible combination of moves """         
        self.printstate(state,"getMoves for .. ")
        
        moves=[]
        name=['A','B','C','D']
        
        #get the filled container names as A,B,C,D
        #generate all combinations -- not so smart ..
        filled=[]
        for i,j in enumerate(state):
            filled.append(name[i])

        #generate possible permutations of moves
        possible_moves=list(itertools.permutations(filled,2))
        #you could use a static list that has all combinations instead
        
        #check if moves are valid, if they are add it to moves
        for m in possible_moves:
        #   print(m)
             if (self.isValidMove(state, m)):
                 moves.append(m)

        # return a list of remaining moves
        return moves
    
    
def main():
    game = Game()
    game.solve()

if __name__ == '__main__':
    main()
