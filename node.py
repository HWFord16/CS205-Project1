import numpy as np

"""
Node class- represents puzzle state, tracks its depth, children and moves from node toward goal state
"""
class Node:
    def __init__(self, state, depth, move = None, parent = None,
                 goal_state = [[1,2,3],[4,5,6],[7,8,0]],
                 misplaced_cost = False, manhattan_cost = False):
        self.g = depth  #g(n) = depth of state
        self.state = state #current puzzle state
        self.move = move  #the operator performed
        self.parent = parent #previous state
        self.children = [] #potential next states
        self.goal_state = goal_state #solve puzzle
        self.misplaced_cost = misplaced_cost #boolean value from user input
        self.manhattan_cost = manhattan_cost #boolean value from user input

        #lamda function to set heuristic h(n) value based on boolean parameter
        if (misplaced_cost): self.h = lambda x: self.misplaced_tiles() #h(n) for A* misplaced tile
        elif (manhattan_cost): self.h = lambda x: self.manhattan() #h(n) for A* Manhattan
        else: self.h = lambda x: 0 #h(n) default for UCS hardcoded to 0. 


    #class functions
    def heuristic(self): return self.g + self.h(self.state)  #heuristic: g(n) + h(n)
    def add_child(self, child_node): self.children.append(child_node) #add child node to current node

    #expand current node and generate all possible child nodes
    def expand(self):
        #find the blank space == (0) value, store its coordinates
        coords = None
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == 0:
                    coords = (i, j)
                    break
            if coords is not None:  #break out of the loop if located (0)
                break

        limit = len(self.state) - 1  #boundary checking for puzzles row/col indexes

        #define operators (moves)
        moves = {
            'down': (1, 0),   #move blank down
            'up': (-1, 0),    #move blank up
            'right': (0, 1),  #move blank right
            'left': (0, -1)   #move blank left
        }

        #generate new states for each node's possible move
        for move, (coord_i, coord_j) in moves.items():
            new_i, new_j = coords[0] + coord_i, coords[1] + coord_j #get new location of blank tile
            if 0 <= new_i <= limit and 0 <= new_j <= limit:  #check new position's bounds are legal
                #check previous move to avoid reversing the last move to create potential cycles etc.
                if not (self.move and move == {'down': 'up', 'up': 'down', 'left': 'right', 'right': 'left'}.get(self.move)):
                    #create new state by copying the current state and swap the blank with adjacent tile
                    new_state = [row[:] for row in self.state]
                    new_state[coords[0]][coords[1]], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[coords[0]][coords[1]]

                    #create new node instance for new state & add as child to parent node
                    new_node = Node(new_state, self.g + 1, move, self,
                                    misplaced_cost = self.misplaced_cost, manhattan_cost = self.manhattan_cost)

                    self.add_child(new_node)

    #calculate #of misplaced tiles in current state
    def misplaced_tiles(self):
        #np array ops. on elements for efficiency
        current_state = np.array(self.state)
        goal_state = np.array(self.goal_state)

        #count non-matching elements between states and return sum
        count = np.sum(current_state != goal_state)
        return count

    #calculate the manhattan distance
    def manhattan(self):
        #map the goal state positions within 3x3 matrix
        goal_dict = dict()
        for i in range(3):
          for j in range(3):
            position = (i*3)+j+1
            if position < 9:      #for 9th element, keep but dont map position due to key errors
              goal_dict[position] = (i, j)

        #Manhattan distance function
        D = lambda x, y: sum([abs(x[i]-y[i]) for i in range(len(x))])

        #calculate total cost
        cost = 0
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
              cell = self.state[i][j]
              if (cell != 0) and (cell in goal_dict): #dont calculate distance for blank element
                cost += D((i, j), goal_dict[cell])

        return cost
