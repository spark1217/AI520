import sys
import os
import math
from queue import PriorityQueue

# Read maze for dfs/bfs. Return maze as array, start position of H, and teleport position
def read_maze_dfs(filename, algo_type):
    file = "Mazes/DFS/" + filename
    start = []
    teleport = []
    maze_array = []
    with open(file) as file:
        for i, line in enumerate(file):
            maze_line = []
            for j, val in enumerate(line.split(',')):
                maze_val = val.strip()
                if maze_val == 'H':
                    start.append([i, j])
                if maze_val == 'T':
                    teleport.append([i, j])
                maze_line.append(maze_val)
            maze_array.append(maze_line)
    return maze_array, start[0], teleport[0]

# Read maze for astar. Return maze as array, start position of H though it is always (0,0), positions of keys and destination
def read_maze_astar(filename, algo_type):
    file = "Mazes/ASTAR/" + filename
    start = []
    keys = []
    goal = []
    maze_array = []
    with open(file) as file:
        for i, line in enumerate(file):
            maze_line = []
            for j, val in enumerate(line.split(',')):
                maze_val = val.strip()
                if maze_val == 'H':
                    start.append([i, j])
                if maze_val == 'K':
                    keys.append([i, j])
                if maze_val == 'D':
                    goal.append([i, j])
                maze_line.append(maze_val)
            maze_array.append(maze_line)
    return maze_array, start[0], keys, goal[0]


# Scenario 0.1 BFS
def find_bfs(maze):
    maze_matrix = maze[0]
    start = maze[1]
    end = maze[2]                        # Goal (x,y)
    visited = []
    visited.append(start)                   # Mark the start position as visited
    queue = [(start, [start])]                            # Store node and path
    count = 0
    path = []                               #final path
    while len(queue) != 0:
        current_location, path = queue.pop(0)            # use FIFO(queue) for bfs
        print(path)
        count += 1
        # Get possible moving direction (adjacent nodes). Neighbors are stored in order by L,R,U,D
        possible_neighbor = find_direction(maze_matrix, current_location[0], current_location[1])       
        
        if current_location not in visited:
            visited.append(current_location)    

        if current_location == end:
            print('Number of paths expanded = ', count)
            return path                                 # Return path once reaching to the goal
       
        for n in possible_neighbor:               # Run neighbors in stored order so that pop queue in preferenced order(L,R,U,D)
            if n not in visited:
                queue.append((n, path+[n]))
                
    if end not in visited:
        print('Number of paths expanded = ', count)
        return ['Not possible']

# Scenario 0.1 DFS
def find_dfs(maze):
    maze_matrix = maze[0]
    start = maze[1]
    end = maze[2]                        # Goal (x,y)
    visited = []
    visited.append(start)                   # Mark the start position as visited
    stack = [(start, [start])]                            # Store node and path
    count = 0
    path = []                               #final path
    while len(stack) != 0:
        current_location, path = stack.pop()            # use LIFO(stack) for dfs
        print(path)
        count += 1
        # Get possible moving direction (adjacent nodes). Neighbors are stored in order by L,R,U,D
        possible_neighbor = find_direction(maze_matrix, current_location[0], current_location[1])       
        
        if current_location not in visited:
            visited.append(current_location)


        if current_location == end:
            print('Number of paths expanded = ', count)
            return path                                 # Return path once reaching to the goal
       
        for n in possible_neighbor[::-1]:               # Run neighbors reversly so that pop stack in preferenced order(L,R,U,D)
            if n not in visited:
                stack.append((n, path+[n]))
        

    if end not in visited:
        print('Number of paths expanded = ', count)
        return ['Not possible']
               


# Scenario 0.1 - find l,r,u,d edge location
def find_direction(maze_matrix, x, y):
    maze_row = len(maze_matrix)
    maze_col = len(maze_matrix[0])
    valid_direction = []
    temp = 0
                
    # left to dead end
    for i in range(y, 0, -1):
        if maze_matrix[x][i-1] == '#':
            temp = i
            if i == y:
                pass
            else:
                valid_direction.append([x, temp])
            break
    
    # right to dead end
    for i in range(y, maze_col):
        if maze_matrix[x][i+1] == '#':
            temp = i
            if i == y:
                pass
            else:
                valid_direction.append([x, temp])
            break
    
    # up to dead end
    for i in range(x, 0, -1):
        if maze_matrix[i-1][y] == '#':
            temp = i
            if i == x:
                pass
            else:
                valid_direction.append([temp, y])
            break
    
    # down to dead end
    for i in range(x, maze_row):
        if maze_matrix[i+1][y] == '#':
            temp = i
            if i == x:
                pass
            else:
                valid_direction.append([temp, y])
            break

    return valid_direction


################################################################################################################
# Scenario 0.2 Astar
def find_astar(maze):
    maze_matrix = maze[0]
    start = maze[1]                     # Should always (0,0)
    keys = maze[2]
    end = maze[3]                        # Goal (x,y)
    maze_row = end[0]
    maze_col = end[1]
    visiting = PriorityQueue()
    current_path = []
    current_path.append(start)
    key_order = []
    # h(n) = manhattan distance (x + y)
    hn_weight = calculate_hn(start, end)
    # g(n) : every movement costs 1
    cost = 0
    astar_weight = hn_weight + cost
    visiting.put([astar_weight, start, current_path, cost], 0)
    
    # Doing astar
    while(visiting.empty() != True):
        get_min = visiting.get()
        current_astar = get_min[0]
        current_location = get_min[1]
        current_path = get_min[2]
        current_cost = get_min[3]
        movement = find_neighbors(maze_matrix, current_location)               # find possible directions
        
        if current_location in keys:
            key_order.append(current_location)
            keys.pop(keys.index(current_location))
            visiting.queue.clear()

        if current_location == end:
            if len(keys) == 0:
                # return cost, collecting order, path
                print('Number of paths expanded = ', current_cost)
                return [key_order, current_cost,  current_path]
            else: 
                # return cost = -1, 'Not possible', key found in order
                current_c
                ost = -1
                print('Number of paths expanded = ', current_cost)
                return [key_order, current_cost, 'Not possible']

        for n in movement:                                              # Check possible directions in preffered order(R,D,L,U)  
            possible_path = []
            possible_path.extend(current_path)
            possible_path.append(n)
            cost = len(possible_path) - 1
            astar_weight = calculate_hn(n, end) + cost
            
            if n in keys:
                # Lowering astar value for Keys by setting heuristic as 0 for key nodes(considering as interim goal) so that Harry choose 'key' location as a priority(new starting point)
                astar_weight=cost
                visiting.put([astar_weight, n, possible_path, cost], astar_weight)
                
            visiting.put([astar_weight, n, possible_path, cost], astar_weight)
            
    if end not in current_path:
        print('Number of paths expanded = ', current_cost)
        return 'Not possible'
    


def calculate_hn(target, end):
    end_x = end[0]
    end_y = end[1]
    x = target[0]
    y = target[1]

    # Heuristic function h(n) = math.sqrt((end_y - y)**2 + (end_x - x)**2)
    hn_weight = math.sqrt((end_y - y)**2 + (end_x - x)**2)
    return hn_weight   


# Scenario 0.2 - Possible moving direction, order by R, D, L, U
def find_neighbors(maze_matrix, current_location):
    x = current_location[0]
    y = current_location[1]
    valid_direction = []
                
    # right
    if y+1 < len(maze_matrix[0]):
        if maze_matrix[x][y+1] != '#':
            valid_direction.append([x, y+1])

    # down   
    if x+1 < len(maze_matrix):
        if maze_matrix[x+1][y] != '#':
            valid_direction.append([x+1, y])        
    
    # left
    if y-1 >=0:
        if maze_matrix[x][y-1] != '#':
            valid_direction.append([x, y-1])
    
    # up
    if x-1 >= 0:
        if maze_matrix[x-1][y] != '#':
            valid_direction.append([x-1, y])
    
    

    return valid_direction






################################################################################################################
# create output file    
def write_solution_file(filename, optimal_output, algo_type):
    # create output 'Solutions' folder if not exists
    directory = "Solutions/" + algo_type +'/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file = directory+filename.strip('.txt')+'_solution.txt'

    # Formatting to desired format for each question
    if algo_type == 'ASTAR':
        with open(output_file, 'w') as f:
            answer = ''
            for i in range(0, len(optimal_output)):
                a = ''
                if type(optimal_output[i]) != int and optimal_output[i] != 'Not possible':
                    for j in range(len(optimal_output[i])):
                        a = ','.join([str(x) for x in optimal_output[i]])
                else:
                    a = optimal_output[i]
                answer = answer + str(a) + '\n'
            f.write(answer.replace('[','(').replace(']',')'))   

    else:
        with open(output_file, 'w') as f:
            answer = ''
            for i in range(0, len(optimal_output)-1):
                answer = answer + str(optimal_output[i]) + ','
            answer = answer + str(optimal_output[len(optimal_output)-1])
            f.write(answer.replace('[','(').replace(']',')'))  




if __name__ == "__main__":
    args = sys.argv[1:]
    filename = args[0]
    algo_type = args[1].upper()
    if algo_type == 'BFS':
        maze = read_maze_dfs(filename, algo_type)
        optimal_output = find_bfs(maze)
    elif algo_type == 'DFS':
        maze = read_maze_dfs(filename, algo_type)
        optimal_output = find_dfs(maze)
    else:
        maze = read_maze_astar(filename, algo_type)
        optimal_output = find_astar(maze)
    
    print(optimal_output)

    # Write solutions
    write_solution_file(filename, optimal_output, algo_type)