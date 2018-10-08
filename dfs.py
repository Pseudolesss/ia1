# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions as dir


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.visited = dict()
        self.path = dict()
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
        self.path.clear()
        
        visited = self.visited.get(state, False)
        
        if visited:
            return visited #add the brand new state and corresponding action to visited
        else:
            path = self.get_path(state)
            self.visited.update(path)
            return path.get(state) #value associated to key state 
    
    def get_path(self, state):
        """
        Given a pacman game state, returns a dictionary.
        Arguments:
        ----------
        - `state`: the current game state.
        Return:
        -------
        - A dictionary with states as keys and directions as values.
        Each state is part of the DFS path solution.
        """
        if state.isWin():
            return {state : dir.STOP}  
        else:
            successors = state.generatePacmanSuccessors()
            self.path.update({state : successors[0][1]})
            self.path.update(self.get_path(successors[0][0]))
            return self.path
