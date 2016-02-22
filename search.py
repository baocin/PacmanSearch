# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    data = util.Stack()
    #states are a combination of position and a the growing list of actions 
    #necessary to get to that position
    data.push((problem.getStartState(),[]))
    
    #The nodes in the graph that have been seen (but not necessarily)
    discovered = []

    while not data.isEmpty():
        currentNode = data.pop()
        #break out the node into its parts for more readable code
        location, actions = currentNode
        
        if problem.isGoalState(location):
            return actions
            
        #if this node is undiscovered then
        if location not in discovered:
            discovered.append(location)   #Add it to the discovered list
            #Add all its children to the stack
            for successor in problem.getSuccessors(location):
                sLocation, sAction, _ = successor
                #Add the action of this node into the list of the parent so that
                # we have a coherent list of what actions are needed to get back
                # to this location
                data.push((sLocation, actions + [sAction]))
                
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    data = util.Queue()
    #states are a combination of position and a the growing list of actions 
    #necessary to get to that position
    data.push((problem.getStartState(),[], 0))
    
    #The nodes in the graph that have been seen (but not necessarily)
    discovered = []

    while not data.isEmpty():
        currentNode = data.pop()
        #break out the node into its parts for more readable code
        location, actions, cost = currentNode
        
        if problem.isGoalState(location):
            return actions
            
        #if this node is undiscovered then
        if location not in discovered:
            discovered.append(location)   #Add it to the discovered list
            #Add all its children to the stack
            for successor in problem.getSuccessors(location):
                sLocation, sAction, sCost = successor
                #Add the action of this node into the list of the parent so that
                # we have a coherent list of what actions are needed to get back
                # to this location
                data.push((sLocation, actions + [sAction], sCost))

def uniformSortByCost_key(a):
    return a[2]
    
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #Same basic structure as dfs and bfs
    Q = util.PriorityQueue()
    # Added cost (the third parameter) back in
    # priority queues need a second weight parameter in function call
    Q.push((problem.getStartState(),[],0), 0)
    discovered = []

    while not Q.isEmpty():
        currentNode = Q.pop()   #Get new node
        location, actions, cost = currentNode   #explode into useful names
        
        #Only terminate when dequeuing a goal
        if problem.isGoalState(location):
            return actions
            
        #Prevents multiple copies of the same node being added to the queue
        if location not in discovered:
            discovered.append(location)
            successors = problem.getSuccessors(location)
            #sortedSuccessors = sorted(successors, key = lambda heu : (heu[2] + heuristic(heu[0], problem)), reverse = False)
            for successor in successors:
                sLocation, sAction, sCost = successor   #explode into names
                #merge the actions lists. Makes it easier to return result
                combinedActions = actions + [sAction]
                #Sum the costs of the actions list so that we can appropriately 
                #sort for the priority queue
                combinedCost = problem.getCostOfActions(combinedActions) + sCost[0]
                Q.push((sLocation, combinedActions, sCost), combinedCost)
                 

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    Q = util.PriorityQueue()
    #Need to calculate the heuristic for the initial state since it could matter
    #Q.push((The begining position, the empty task list, the value of the current start state), and then the cost)
    Q.push((problem.getStartState(),[],heuristic(problem.getStartState(), problem)), 0)
    discovered = []

    while not Q.isEmpty():
        currentNode = Q.pop()
        location, actions, cost = currentNode   #explode into useful names
        
        #Only terminate when dequeuing a goal
        if problem.isGoalState(location):
            return actions
            
        #Prevents multiple copies of the same node being added to the queue
        if location not in discovered:
            discovered.append(location)
            successors = problem.getSuccessors(location)
            #sortedSuccessors = sorted(successors, key = lambda heu : (heu[2] + heuristic(heu[0], problem)), reverse = False)
            for successor in successors:
                sLocation, sAction, sCost = successor
                #merge the actions lists. Makes it easier to return result
                combinedActions = actions + [sAction]
                #Sum the costs of the actions list so that we can appropriately 
                #sort for the priority queue
                combinedCost = problem.getCostOfActions(combinedActions) + heuristic(sLocation, problem)
                Q.push((sLocation, combinedActions, sCost), combinedCost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
