import os
import sys
from queue import PriorityQueue
import random
    

# Read maze. Return maze as array.
def read_maze(filename):
    file = "Mazes/" + filename
    maze_array = []
    with open(file) as file:
        for i, line in enumerate(file):
            maze_line = []
            for j, val in enumerate(line.split(',')):
                maze_val = val.strip()
                maze_line.append(maze_val)
            maze_array.append(maze_line)
    return maze_array

# Possible moving direction, order by L, R, U, D
def find_neighbors(maze, x, y):
    maze_row = len(maze)
    maze_col = len(maze[0])
    weight = int(maze[x][y])
    valid_direction = []
                
    # left
    if y-weight >= 0: 
        valid_direction.append([x, y-weight])
    
    # right
    if y+weight < maze_col:  
        valid_direction.append([x, y+weight])
    
    # up 
    if x-weight >= 0: 
        valid_direction.append([x-weight, y])
    
    # down 
    if x+weight < maze_row: 
        valid_direction.append([x+weight, y])

    return valid_direction

# Heuristic 1 - 1 if in the same row/column as the goal, 2 otherwise
def h1_cal(goal, target):
    h1 = 0
    if target == goal:
        h1 = 0
    elif target[0] == goal[0] or target[1] == goal[1]:
        h1 = 1
    else:
        h1 = 2
    return h1

# Heuristic 2 - manhattan distance
def h2_cal(goal, target):
    h2 = abs(goal[1]-target[1]) + abs(goal[0]-target[0])
    return h2




def hill_climbing(maze, algo_type):
    maze_row = len(maze) -1
    maze_col = len(maze[0]) -1
    goal = [maze_row, maze_col]
    search_limit = [500,600,700,800,900,1000]
    num_restart = [10,15,20,25]
    prob_of_best_node = [0.2, 0.4, 0.6, 0.8]

    # Doing normal hill climbing and make output
    if algo_type == 'HC':
        final_output = ''
        for sl in search_limit:
            # start position (0,0)
            h1_result = sac_hc(maze, [0,0], goal, 'h1', sl)
            h2_result = sac_hc(maze, [0,0], goal, 'h2', sl)
            # Formatting solutions
            if h1_result[0]=='Not Possible':
                h1_path = 'Not Possible'
            else:
                h1_path = ','.join(str(x) for x in h1_result[0]) 
            if h2_result[0] == 'Not Possible':
                h2_path = 'Not Possible'
            else:
                h2_path = ','.join(str(x) for x in h2_result[0]) 
            print_output = 'Number of iterations : ' + str(sl) + '\nH1 \nPath : ' +  h1_path + '\nNumber of visited nodes : ' + str(h1_result[1]) + '\n \nH2 \nPath : ' +  h2_path + '\nNumber of visited nodes : ' + str(h2_result[1]) + '\n \n'
            final_output += print_output
        return final_output

    # Doing random restart hill climbing and make output
    elif algo_type == 'RR':
        final_output = ''
        for sl in search_limit:
            for nr in num_restart:
                random.seed(1234)
                h1_result = sac_rr(maze, goal, 'h1', sl, nr)
                h2_result = sac_rr(maze, goal, 'h2', sl, nr)
                # formatting solutions
                print_output = 'Number of iterations : ' + str(sl) + ' \n' + 'Number of restart : ' + str(nr) + '\n' + 'H1' + '\n'
                for i in range(len(h1_result[0])):
                    print_output += 'Iteration ' + str(i+1) + ' with start position as ' + str(h1_result[0][i]) + '\n'
                if h1_result[1]=='Not Possible':
                    h1_path = 'Not Possible'
                else:
                    h1_path = ','.join(str(x) for x in h1_result[1])
                print_output += 'Path : ' + h1_path + '\n' + 'Number of visited nodes : ' + str(h1_result[2]) + '\n' + '\n'
                print_output += 'H2' + '\n' 
                
                for j in range(len(h2_result[0])):
                    print_output += 'Iteration ' + str(j+1) + ' with start position as ' + str(h2_result[0][j]) + '\n'
                if h2_result[1]=='Not Possible':
                    h2_path = 'Not Possible'
                else:
                    h2_path = ','.join(str(x) for x in h2_result[1])
                print_output += 'Path : ' + h2_path + '\n' + 'Number of visited nodes : ' + str(h2_result[2]) + '\n' + '\n'
                final_output = final_output + print_output
        return final_output

    # Doing random walk hill climbing and make output
    elif algo_type == 'RW':
        final_output = ''
        for sl in search_limit:
            for p in prob_of_best_node:
                random.seed(1234)
                # start position (0,0)
                h1_result = sac_rw(maze, [0,0], goal, 'h1', sl, p)
                h2_result = sac_rw(maze, [0,0], goal, 'h2', sl, p)
                # formatting solutions
                print_output = 'Number of iterations : ' + str(sl) + ' \n' + 'Probability value chosen : ' + str(p) + '\n' + 'H1' + '\n'
                for i in range(len(h1_result[2])):
                    print_output += str(h1_result[2][i][1]) + ' move : ' + str(h1_result[2][i][0]) + '\n'
                if h1_result[0]=='Not Possible':
                    h1_path = 'Not Possible'
                else:
                    h1_path = ','.join(str(x) for x in h1_result[0]) 
                print_output += 'Path : ' + h1_path + '\n' + 'Number of visited nodes : ' + str(h1_result[1]) + '\n' + '\n'
                print_output += 'H2' + '\n' 
                for j in range(len(h2_result[2])):
                    print_output += str(h2_result[2][j][1]) + ' move : ' + str(h2_result[2][j][0]) + '\n'
                if h2_result[0] == 'Not Possible':
                    h2_path = 'Not Possible'
                else:
                    h2_path = ','.join(str(x) for x in h2_result[0]) 
                print_output += 'Path : ' + h2_path + '\n' + 'Number of visited nodes : ' + str(h2_result[1]) + '\n' + '\n'
                final_output = final_output + print_output
        return final_output




## 1. STEEPEST ASCENT HILL CLIMBING #################################################################################################
# Implemented based on the pseudocode from the textbook
# function HILL-CLIMBING(problem) returns a state that is a local maximum
#  current ← problem.INITIAL-STATE
#  loop do
#    neighbor ← a highest-valued successor of current
#    if VALUE(neighbour) ≤ VALUE(current) then return current
#    current ← neighbor
#####################################################################################################################################
def sac_hc(maze, start, goal, heuristic, search_limit):
    current = start
    current_x, current_y = start[0], start[1]
    if heuristic == 'h1':
        initial_value = h1_cal(goal, start)
    elif heuristic == 'h2':
        initial_value = h2_cal(goal, start)
    current_value = initial_value
    limit = search_limit                           # Search limit
    count = 1                               # Start with 1. This counts starting node as visited.
    path = []
    path.append(start) 
    neighbor_queue = PriorityQueue()
    while current != goal:                  # Loop until reaching to the goal
        
        if count == limit:                  # Return fail if solution is not found within number of search limit
            return ['Not Possible', count]
        
        neighbors = find_neighbors(maze, current_x, current_y)
        for n in neighbors:
            if heuristic == 'h1':
                hn = h1_cal(goal, n)
            elif heuristic == 'h2':
                hn = h2_cal(goal, n)
            neighbor_queue.put([hn, neighbors.index(n), n])     # Set first priority=heuristic value, second priority=direction preference

        # Get best neighbor
        highest_successor = neighbor_queue.get()
        highest_successor_value = highest_successor[0]
        highest_successor_node = highest_successor[2]

        # Do hill climbing
        if highest_successor_value <= current_value:
            current_value = highest_successor_value
            current_x,  current_y = highest_successor_node[0], highest_successor_node[1]
            current = highest_successor_node
            path.append(current)
            count += 1
            neighbor_queue.queue.clear() 
              

    return [path, count]





## 2. STEEPEST ASCENT HILL CLIMBING WITH RANDOM RESTART ################################################################################################3
def sac_rr(maze, goal, heuristic, search_limit, num_restart):
    current = generate_random_state(maze)
    current_x, current_y = current[0], current[1]
    if heuristic == 'h1':
        initial_value = h1_cal(goal, current)
    elif heuristic == 'h2':
        initial_value = h2_cal(goal, current)
    current_value = initial_value
    restart = num_restart                            # number of random restarts
    limit = search_limit                            # Search limit
    count = 1                               # Start with 1. This counts starting node as visited.
    temp = 0
    path = []
    path.append(current) 
    neighbor_queue = PriorityQueue()
    iteration = []                          # Track randomly choosen nodes
    iteration.append(current)

    while current != goal:                  # Loop until reaching to the goal
        if temp == limit:
            neighbor_queue.queue.clear()                # Revert back to initial status before restart
            path = []
            current = generate_random_state(maze)       # Choose restarting node randomly if solution is not found
            
            iteration.append(current)
            path.append(current)
            current_x, current_y = current[0], current[1]
            if heuristic == 'h1':
                current_value = h1_cal(goal, n)
            elif heuristic == 'h2':
                current_value = h2_cal(goal, n)
            restart -= 1
            temp = 0
            if restart == 0:
                path = 'Not Possible'                          
                return [iteration, path, count]

        neighbors = find_neighbors(maze, current_x, current_y)
        for n in neighbors:
            if heuristic == 'h1':
                hn = h1_cal(goal, n)
            elif heuristic == 'h2':
                hn = h2_cal(goal, n)
            neighbor_queue.put([hn, neighbors.index(n), n])             # Set first priority=heuristic value, second priority=direction preference
            

        # Get best neighbor
        highest_successor = neighbor_queue.get()
        highest_successor_value = highest_successor[0]
        highest_successor_node = highest_successor[2]

        # Do hill climbing
        if highest_successor_value <= current_value:
            current_value = highest_successor_value
            current_x,  current_y = highest_successor_node[0], highest_successor_node[1]
            current = highest_successor_node
            path.append(current)
        count += 1
        temp += 1

    return [iteration, path, count]

# Choose restarting node randomly
def generate_random_state(maze):
    row_random = random.randint(0, len(maze) - 1)
    col_random = random.randint(0, len(maze[0]) - 1)
    return [row_random, col_random]




## 3. STEEPEST ASCENT HILL CLIMBING WITH RANDOM WALK #################################################################################################
# Given p, choose best value with p. [Best, Random] = [p, 1-p]
# If choose random, equal distribution for neighborsx
######################################################################################################################################################

def sac_rw(maze, start, goal, heuristic, search_limit, prob_of_best_node):
    current = start
    current_x, current_y = start[0], start[1]
    if heuristic == 'h1':
        initial_value = h1_cal(goal, start)
    elif heuristic == 'h2':
        initial_value = h2_cal(goal, start)
    current_value = initial_value
    limit = search_limit                           # Search limit
    count = 1                               # Start with 1. This counts starting node as visited.
    move = []
    path = []
    path.append(start) 
    neighbor_queue = PriorityQueue()
    while current != goal:                  # Loop until reaching to the goal
        if count == limit:                  # Return fail if solution is not found within number of search limit
            return ['Not Possible', count, move]
        
        neighbors = find_neighbors(maze, current_x, current_y)          # Get neighbors
        for n in neighbors:
            if heuristic == 'h1':
                hn = h1_cal(goal, n)
            elif heuristic == 'h2':
                hn = h2_cal(goal, n)
            neighbor_queue.put([hn, neighbors.index(n), n])     # Set first priority=heuristic value, second priority=direction preference


        # Choose best or random move with given probability and 1-probability
        random_or_best = find_random_or_best(['Best', 'Random'], [prob_of_best_node, 1-prob_of_best_node])
        if random_or_best[0] == 'Best':
            # If best move is selected, choose best neighbor
            next_move, next_value = get_best_neighbor(neighbor_queue)
        elif random_or_best[0] == 'Random':
            # If random move is selected, choose random neighbor
            next_node_random = find_random_neighbor(current, neighbors)
            next_move = next_node_random[0]
            if heuristic == 'h1':
                next_value = h1_cal(goal, next_move)
            elif heuristic == 'h2':
                next_value = h2_cal(goal, next_move)
        
        # Do hill climbing
        if next_value <= current_value:
            current_value = next_value
            current_x,  current_y = next_move[0], next_move[1]
            current = next_move
            move.append([current, random_or_best[0]])
            path.append(current)
            count += 1  
            neighbor_queue.queue.clear() 
    return [path, count, move]



def get_best_neighbor(neighbor_queue):
    best = neighbor_queue.get()
    best_value = best[0]
    best_node = best[2]

    return best_node, best_value
    

def find_random_or_best(choice, probability):
    return random.choices(choice, probability)

def find_random_neighbor(current, neighbors):
    # calculate equal probability of possible neighbors
    p = 1/len(neighbors)
    prob = []
    for i in neighbors:
        prob.append(p)
    return random.choices(neighbors, prob)



# create output file 
def write_solution_file(filename, optimal_output, algo_type):
    # create output 'Solutions' folder if not exists
    directory = "Solutions/" + algo_type +'/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file = directory+filename.strip('.txt')+'_solution.txt'
    with open(output_file, 'w') as f:
        f.write(optimal_output.replace('[','(').replace(']',')'))  
        



if __name__ == "__main__":
    args = sys.argv[1:]
    filename = args[0]
    algo_type = args[1].upper()     #hc, rr, rw
    maze = read_maze(filename)
    optimal_output = hill_climbing(maze, algo_type)

    # print(optimal_output)
    # Write solutions
    write_solution_file(filename, optimal_output, algo_type)
