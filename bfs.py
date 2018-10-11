# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions as dir
import queue


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.computed = dict() # Dict to store computed actions {(s.PacmanPos, s.food) : action}
        self.visited = set() # Set to store the visited nodes
        self.queue = queue.Queue() # FIFO queue
        self.args = args

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.
        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        key = ( state.getPacmanPosition(), state.getFood() ) #key for dict
        
        computed = self.computed.get(key, False)
        
        if computed:
            return computed #return already computed result
        else:
            self.visited.clear() # Clear set if previously used
            self.queue = queue.Queue() # Brand new queue
            
            self.queue.put( ( state, {} ) )
            path = self.get_path()
            
            self.computed.update(path) # Keep computed answers
            return path.get(key) #value associated to key (position, food)

    def get_path(self):
        """
        Given a pacman game state, returns a legal move.
        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        while True:
            pair = self.queue.get() # Pop out the first element of the FIFO self.queue
            state = pair[0] # Consider the state linked to the first element
            visited = pair[1] # Path to the state as dict {key : actions}
            key = (state.getPacmanPosition(), state.getFood()) # for dict and set
            
            if state.isWin():
                visited[key] = dir.STOP # add {(s.Pacman pos , s.food) : action} to the returned dict
                return visited
            
            else:
                successors = state.generatePacmanSuccessors()
                
                if key in self.visited: # If actual state already visited
                    continue # Ignore this node
                
                self.visited.add(key)
                
                for son in successors:
                    son_key = (son[0].getPacmanPosition(), son[0].getFood())
                    if son_key in self.visited: #If son visited
                        continue # Next son
                    visited_aux = visited.copy() # Buffer to avoid losing original dict data may be long to copy after the 1st son
                    visited_aux[key] = son[1] # Add the action of the current state
                    self.queue.put((son[0], visited_aux))