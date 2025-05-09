from search import graph_search


"""
User interface for interacting w/ 8-puzzle
"""
def main():
    print("Welcome to Harrison's 8-puzzle solver\n")

    while True:
        #initialize puzzle variables
        initial_state = []
        goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        problem = (initial_state, goal_state)

        #prompt User Input for Puzzle
        choicePuzzle = input('Type "1"- to use a default puzzle or Type "2"- to enter your own puzzle: ')

        while choicePuzzle not in ('1','2'):
          choicePuzzle = input('Invalid Choice. Type "1" to use a default puzzle or "2" to enter your own puzzle : ')

        #default puzzle (more than trivial)
        if choicePuzzle == "1":
          initial_state.append([8, 7, 1])
          initial_state.append([6, 0, 2])
          initial_state.append([5, 4, 3])

        elif choicePuzzle == "2":
            print('Enter your puzzle, use a zero (0) to represent the blank.')
            for i in range(3):
                row = input('Enter row ' + str(i+1) + ', use spaces between numbers: ')
                initial_state.append([int(num) for num in row.split()])


        while (choicePuzzle == '1' or choicePuzzle == '2'):
            #prompt User Input for Algorithm Choice
            print('\nAlgorithms List\n______________________')
            print('1. Uniform Cost Search')
            print('2. A* with the Misplaced Tile heuristic')
            print('3. A* with the Manhattan distance heuristic')
            print('\nEnter your choice of algorithm:')
            algorithmChoice = input()

            if algorithmChoice == '1':
                print("\n Generating Solution Steps\n\n")
                depth,maxFrontier,nodesExpanded= graph_search(problem)
                break
            elif algorithmChoice == '2':
                print("\n Generating Solution Steps\n\n")
                depth,maxFrontier,nodesExpanded= graph_search(problem, misplaced_tiles=True)
                break
            elif algorithmChoice == '3':
                print("\n Generating Solution Steps\n\n")
                depth,maxFrontier,nodesExpanded= graph_search(problem, manhattan=True)
                break
            else:
                print('\nInvalid. Select an algorithm by entering a number 1-3:')
                algorithmChoice = input()

        print(f"\nDepth of Solution: {depth}")
        print(f"Maximum Frontier Size: {maxFrontier}")
        print(f"Total States Expanded: {nodesExpanded}")

        #check if user wants to continue or exit
        cont = input('\nWould you like to solve another puzzle? (Y/N): ')
        if cont.upper() != 'Y':
            print("\n\nThanks for Playing!\n\n")
            break

if __name__ == '__main__':
    main()