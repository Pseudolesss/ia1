# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions as dir
from heapq import heappush, heappop

class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.computed = dict() # Dict to store computed actions {(s.PacmanPos, s.food) : action}
        self.visited = set() # Set to store the visited nodes
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
            
            q = []
            heappush(q,(0, (state, {}, 0)) ) # Initial state of the priority queue
            path = self.get_path(q)
            
            self.computed.update(path) # Keep computed answers
            return path.get(key) #value associated to key (position, food)
    
    def get_path(self, queue):
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
        i = 0 # Implicit value to avoid identical priority in the priority queue
        
        while True:
            entry = heappop(queue) # Pop out the priority element of the priority queue
            state = entry[1][0] # Consider the state linked to the first element
            cost = entry[1][2] # Accumulated cost for this state
            visited = entry[1][1] # Path to the state as dict {key : actions}
            key = (state.getPacmanPosition(), state.getFood()) # for dict

            if state.isWin():
                visited[key] = dir.STOP
                return visited
            
            else:
                
                if key in self.visited: # If actual state already visited
                    continue # Ignore this node
    
                self.visited.add(key)
    
                successors = state.generatePacmanSuccessors()
                
                for son in successors:
                    son_key = (son[0].getPacmanPosition(), son[0].getFood())
                    if son_key in self.visited: #If son visited
                        continue # Next son
                    if son[0].isWin():
                        visited[key] = son[1] # add {(s.Pacman pos , s.food) : action} of the current node to the returned dict
                        visited[(son[0].getPacmanPosition(), son[0].getFood())] = dir.STOP # of the final node
                        return visited
                    i+=10**-12
                    visited_aux = visited.copy() # Buffer to avoid losing original dict data after the 1st son
                    visited_aux[key] = son[1] # Add the action of the current state
                    new_priority = cost + 1 + i + self.estimated_cost(son_key[0], son_key[1])
                    heappush( queue, (new_priority, ( son[0], visited_aux, cost + 1)) )
    
    
    def estimated_cost(self, pos, foods):
        """
        Given a pacman position and a food matrix, returns the shortest
        distance to a dot.
        Arguments:
        ----------
        - `pos`: Pacman position as a pair (x,y) x,y >= 0
        - `food`: matrix of booleans indicating by True values the presence 
        of a dot in the maze.
        Return:
        -------
        - A integer representing the longest distance to a dot
        """
        foods_pos = []
        i=0 # x values
        for rows in foods:
            j=0 # y values
            for elem in rows:
                if elem:
                    foods_pos.append((i,j))
                j+=1
            i+=1

        distances = list( map( lambda x : abs(pos[0] - x[0]) + abs(pos[1] - x[1]) ,foods_pos) )
        return max(distances)