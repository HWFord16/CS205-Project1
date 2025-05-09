import heapq
from node import Node
from tree import Tree


"""
Driver Code for generic search algorithm
Perfroms UCS by default, A* Misplaced or Manhattan based on boolean parameters
"""
def graph_search(problem, misplaced_tiles = False, manhattan = False, output_path = True):
    initial_state = problem[0]
    goal_state = problem[1]

    frontier = []
    explored = set()
    num_nodes_expanded = 0
    max_frontier_size = 0

    #helper func. to convert lists of lists to tuples tuple for quicker comparisons by hashing
    def t(x): return tuple(tuple(y) for y in x)

    #initialize root node in tree for frontier
    initial_node = Node(initial_state, depth=0, goal_state=goal_state,
                        misplaced_cost = misplaced_tiles, manhattan_cost = manhattan)

    tree = Tree(initial_node) #instantiate tree object for solution tracing

    #utilize priority queue, counter for unique order/ties and insert root node
    heapq.heappush(frontier,(initial_node.heuristic(), 0, t(initial_state), initial_node))
    counter =1 
    frontierState = {t(initial_state): initial_node}

    #execute loop while frontier is not empty
    while(frontier):
        #pick & remove from frontier
        _,_,state,current_node = heapq.heappop(frontier)

        #test goal state, output solution path and return the depth, time & space data
        if (state == t(goal_state)):
          if (output_path):
            tree.output_solution(current_node) #trace solution path from goal node to root
          return (current_node.g, max_frontier_size, num_nodes_expanded)

        if state in explored: continue #skip state if is already explored
        else: explored.add(state)  #set current state to "explored"

        #expand
        current_node.expand()
        num_nodes_expanded += 1                                   #node count
        max_frontier_size = max(max_frontier_size, len(frontier)) #frontier size

        #iterate through all children of current node 
        for child in current_node.children: 
            child_state_t = t(child.state) #convert child state to hashable tuple
            if child_state_t not in explored and child_state_t not in frontierState: #ensure child repeated
                heapq.heappush(frontier,(child.heuristic(),counter, child_state_t,child)) #add child to heap
                frontierState[child_state_t] = child #add child state
                counter += 1 #adjust counter for unique ordering in heap
    return False

### manual tracking of min() cost via dictionaries ###
# def graph_search(problem, misplaced_tiles = False, manhattan = False, output_path = True):
#     initial_state = problem[0]
#     goal_state = problem[1]

#     frontier = dict()
#     explored = dict()
#     num_nodes_expanded = 0
#     max_frontier_size = 0

#     #helper func. to convert lists of lists to tuples tuple for quicker comparisons by hashing
#     def t(x): return tuple(tuple(y) for y in x)

#     #initialize root node in tree for frontier
#     initial_node = Node(initial_state, depth=0, goal_state=goal_state,
#                         misplaced_cost = misplaced_tiles, manhattan_cost = manhattan)

#     tree = Tree(initial_node) #instantiate tree object for solution tracing
#     frontier[t(initial_state)] = initial_node #add root node to frontier

#     #execute loop while frontier is not empty
#     while(frontier):
#         #pick & remove from frontier using minimum heuristic function cost 
#         min_cost = min(frontier[x].heuristic() for x in frontier)
#         pick_state = next(state for state in frontier if frontier[state].heuristic() == min_cost and state not in explored)

#         #test goal state, output solution path and return the depth, time & space data
#         if (t(pick_state) == t(goal_state)):
#           if (output_path):
#             tree.output_solution(frontier[t(pick_state)]) #trace solution path from goal node to root
#           return (frontier[t(pick_state)].g, max_frontier_size, num_nodes_expanded)

#         #expand node 
#         frontier[t(pick_state)].expand()

#         num_nodes_expanded += 1                                   #node count
#         max_frontier_size = max(max_frontier_size, len(frontier)) #frontier size

#         #pick node in frontier run the chosen algorithm from func. param
#         for child in frontier[t(pick_state)].children:
#             child_state_t = t(child.state)
#             if child_state_t not in explored and child_state_t not in frontier:
#                 frontier[child_state_t] = child

#         #set current state to "explored" and remove from frontier
#         explored[t(pick_state)] = True
#         del frontier[t(pick_state)]

#     return False
