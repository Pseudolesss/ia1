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
        key = ( state.getPacmanPosition(), state.getFood() ) #key for dict
        self.path.clear() #clear obsolete results
        
        visited = self.visited.get(key, False)
        
        if visited:
            return visited[1] #return already compute result
        else:
            path = self.get_path(state)
            return path.get(key)[1] #value associated to key (position, food) 
    
    def get_path(self, state):
        """
        Given a pacman game state, returns a dictionary.
        Arguments:
        ----------
        - `state`: the current game state.
        Return:
        -------
        - A dictionary with pair (Pacman pos, food pos) as keys and coresponding states
        and directions pairs as values.
        Each state is part of the DFS path solution starting from state.
        """        
        print(state)
        print( state.isWin())
        if state.isWin():
            return { ( state.getPacmanPosition(), state.getFood() ) : (state, dir.STOP)}  
        else:
            successors = state.generatePacmanSuccessors()
            
            for son in successors:
                key = (son[0].getPacmanPosition(), son[0].getFood())
                if not self.visited.get(key, False):
                    self.visited.update({key : (state, son[1])}) #add the brand new states and corresponding actions to visited
                    break
            
            self.path.update({key : (state, son[1])})
            self.path.update(self.get_path(son[0]))
            return self.path
