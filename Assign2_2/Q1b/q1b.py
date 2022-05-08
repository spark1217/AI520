import os
import sys
from queue import PriorityQueue
from sys import maxsize




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
def find_neighbors(maze_matrix, x, y):
    maze_row = len(maze_matrix)
    maze_col = len(maze_matrix[0])
    weight = int(maze_matrix[x][y])
    if weight == 0:
        return []
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

# Heuristic - manhattan distance
def hn_cal(goal, target):
    hn = abs(goal[1]-target[1]) + abs(goal[0]-target[0])
    return hn

# RBFS
def recursive_best_first_search(maze):
    start_state = [0,0]
    maze_row = len(maze) -1
    maze_col = len(maze[0]) -1
    global goal
    goal = [maze_row, maze_col]
    backtracking = 0
    global result
    result = ''
    
    global queue 
    queue = []

    global node_selected
    node_selected = []
    global visited
    visited = []
    global nodef
    nodef=hn_cal(goal, start_state)
    output, fvalue, backtracking = RBFS(start_state, maxsize, backtracking, nodef)
    final_output = output_format(visited)
    print('# of backtracking: ', backtracking)
    return final_output



def RBFS(current, f_limit, backtracking, nodef, cost=0, alternative_f=maxsize):
    # Tracking visited node, f value, alternative f value, and its neighbors
    visited.append([current,nodef,alternative_f,find_neighbors(maze, current[0], current[1])])
    # If meet the goal, terminate
    if current == goal:
        return [current, f_limit, backtracking]
    
    neighbors = find_neighbors(maze, current[0], current[1])  
    if len(neighbors)==0:
        return [None, maxsize, backtracking]

    # add neighbors to successors queue
    successors = []
    for n in neighbors:
        cost += 1
        child_f = hn_cal(goal,n)+cost
        successors.append((child_f, neighbors.index(n), n))   # Set first priority=heuristic value, second priority=direction preference
        cost -= 1


    # Check if successors is empty --> return fail
    if len(successors)==0:
        result = 'Fail'
        return [result, maxsize, backtracking]


       
    while successors:

        successors.sort()
        # Find successor with minimum f value
        best=successors[0][2]
        best_index=successors[0][1]
        best_f=successors[0][0]
        # Add all possible alternatives to queue (explore unexplored alternatives)
        queue.append(successors[0])
        if best_f > f_limit:
            result = 'Fail'
            backtracking += 1
            cost -= 1
            return [result, best_f, backtracking]
        
        
        
        # Find successor with second minimum f value
        alternative=successors[1][2]
        alternative_index=successors[1][1]
        alternative_f=successors[1][0]
        # Add all possible alternatives to queue (explore unexplored alternatives)
        queue.append(successors[1])

        
        # Pick alternatives from all unexplored alternatives and use as alternative_f
        queue.sort()
        queue.pop(0)
        second_best = queue[0][2]
        second_index = queue[0][1]
        second_f = queue[0][0]

        # Recursive call of RBFS        
        s = RBFS(best, min(f_limit, second_f), backtracking, nodef=best_f, cost=cost+1, alternative_f=second_f)
        # Result of recursive call
        result = s[0]
        best_f = s[1]
        backtracking = s[2]

        successors[0] = (best_f, best_index, best)     
        queue.pop(0)
        if result != 'Fail':
            return [result, best_f, backtracking]
    

# Formatting output
def output_format(solution):
    o = ''
    for i in solution:
        o += 'Node Selected: ' + str(i[0]) + '\nF-Value: ' + str(i[1]) + ' , alternative_best_f: ' + str(i[2]) + '\n' 
        if len(i[3])>0:
            o += 'Further Child Nodes: '
            for j in range(len(i[3])):
                o += str(i[3][j]).replace(' ','')
            o += ',\n-----------------------------------\n'

    return o


# create output file    
def write_solution_file(filename, optimal_output):
    # create output 'Solutions' folder if not exists
    directory = "Solutions/" 
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file = directory+filename.strip('.txt')+'_solution.txt'
    with open(output_file, 'w') as f:
        f.write(optimal_output)  
        



if __name__ == "__main__":
    filename = sys.argv[1]
    global maze
    maze = read_maze(filename)
    optimal_output = recursive_best_first_search(maze)
    print(optimal_output)

    # Write solutions
    write_solution_file(filename, optimal_output)
