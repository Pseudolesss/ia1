from pacman_module.game import Agent
from pacman_module.pacman import Directions as dir


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
        - `state`: the current game state.
                   
        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        key = (state.getPacmanPosition(), state.getFood()) # Key for dict
        computed = self.computed.get(key, False)
        
        if computed:
            return computed # Return already computed result
        else:
            path = self.get_path(state, [])
            self.computed.update(path)
            return path.get(key) # Value associated to key (position, food) 
    
    def get_path(self, state, visited):
        """
        Given a pacman game state, returns a dictionary.
        
        Arguments:
        ----------
        - `state`: the current game state.
        
        Return:
        -------
        - A dictionary with pairs (Pacman pos, food pos) as keys and actions as
        values.
        
        Each key originates from a state that is part of the DFS path solution
        starting from the argument state.
        """
        visited.append((state.getPacmanPosition(), state.getFood()))
        
        if state.isWin():
            return {(state.getPacmanPosition(), state.getFood()) : dir.STOP} 
        else:
            path = dict()
            next_call = dict()
            successors = state.generatePacmanSuccessors()
            i=0
            
            for son in successors:
                if not (son[0].getPacmanPosition(), son[0].getFood()) in visited:
                    next_call = self.get_path(son[0], visited)
                    if len(next_call) == 0:
                        i+=1 # No solution from there
                        continue
                    break
                i+=1 # Already visited (avoids cycles)
                
            if i == len(successors): # No son converges to solution
                return dict()
            
            key = (state.getPacmanPosition(), state.getFood())
            path.update({key : son[1]}) # Addition of the {state : action} of
                                        # the current call 
            path.update(next_call) # Add result of the selected son
            return path