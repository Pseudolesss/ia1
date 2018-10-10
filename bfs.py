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
        self.computed = dict()
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
            q = queue.Queue()
            q.put( ( state, {} ) )
            path = self.get_path(q)
            self.computed.update(path)
            return path.get(key) #value associated to key (position, food)

    def get_path(self, list_visited):
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
            pair = list_visited.get() # Pop out the first element of the FIFO queue
            state = pair[0] # Consider the state linked to the first element
            visited = pair[1] # Path to the state as dict {key : actions}
            key = (state.getPacmanPosition(), state.getFood()) # for dict
            
            if state.isWin():
                visited[key] = dir.STOP # add {(s.Pacman pos , s.food) : action} to the returned dict
                return visited
            
            else:
                successors = state.generatePacmanSuccessors()
                
                for son in successors:
                    visited_aux = visited.copy() # Buffer to avoid losing original dict data after the 1st son
                    visited_aux[key] = son[1] # Add the action of the current state
                    list_visited.put((son[0], visited_aux))