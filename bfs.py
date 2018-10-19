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
        self.computed = dict() # Dict to store computed actions
                               # {(s.PacmanPos, s.food) : action}
        self.visited = set() # Set to store the visited nodes
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
            self.visited.clear() # Clear set if previously used
            q = queue.Queue() # FIFO queue
            q.put((state, {})) # Initial state of the queue
            path = self.get_path(q)
            self.computed.update(path) # Keep computed answers
            return path.get(key) # Value associated to key (position, food)

    def get_path(self, q):
        """
        Arguments:
        ----------
        - 'q' : A FIFO queue which stores 
        (state, {(Pacman pos, Food pos): action}) elements. 
        
        Return:
        -------
        - A dictionary with pairs (Pacman pos, food pos) as keys and actions as
        values.
        
        Each key originates from a state that is part of the BFS path solution
        starting from the argument state.
        """
        while True:
            pair = q.get() # Pop out the first element of the FIFO self.queue
            state = pair[0] # Consider the state linked to the first element
            visited = pair[1] # Path to the state as dict {keys : actions}
            key = (state.getPacmanPosition(), state.getFood()) # For dict and
                                                               # set
            
            if state.isWin():
                visited[key] = dir.STOP # Add {(s.PacmanPos, s.food) : action}
                                        # to the returned dict
                return visited

            else:
                
                if key in self.visited: # If actual state already visited
                    continue # Ignore this node
                
                successors = state.generatePacmanSuccessors()
                self.visited.add(key)
                
                for son in successors:
                    son_key = (son[0].getPacmanPosition(), son[0].getFood())
                    
                    if son_key in self.visited: # If son visited
                        continue # Next son

                    visited_aux = visited.copy() # Buffer to avoid losing
                                                 # original dict

                    visited_aux[key] = son[1] # Add the action of the current
                                              # state
                    q.put((son[0], visited_aux))