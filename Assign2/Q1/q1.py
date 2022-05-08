import os
import sys
from queue import PriorityQueue

def read_table(filename):
    # read txt files. txt files must be in the same folder with py file.
    distance_input_tables = open(filename,'r')
    return distance_input_tables

# Read h(n) from txt file. dic_hn will only contain nodes, in the format of {node:heuristic}
def find_hn(distance_input_tables):
    hn_input_table = []
    dic_hn = {}
    for hn in distance_input_tables:
        hn_list = hn.replace('\n','').replace(' ','').split(',')            # text processing. removing new line and empty spaces then split by a comma
        if hn_list == ['']:                         # Stop reading once it reaches empty line, which implies to the end of the heuristic(h(n)) table
            break
        if hn_list[0] == 'Node':                    # Skip unnecessary heading line
            pass
        else:
            dic_hn[hn_list[0]]=int(hn_list[1])
    return dic_hn


# Read g(n) from txt file. gn_input_table
def find_gn(distance_input_tables):
    gn_input_table = []
    for gn in distance_input_tables:
        gn_list = gn.replace('\n','').replace(' ','').split(',')            # text processing. removing new line and empty spaces then split by a comma
        if len(gn_list) == 3:                       # Since g(n) table has 3 columns
            gn_input_table.append(gn_list)  
    return gn_input_table[1:]                       # Skip unnecessary heading line


# return sum of g(n) for each path
def find_path_weight(output_path, gn):
    path_weight = 0
    path = []
    
    # Path is stored in string format. Find substring G1, G2 and temporarily replace to avoid making G1 and G2 to separate nodes of G and 1 and 2
    output_path = output_path.replace('G1','1').replace('G2','2')
    # Convert string to list to find the distance between each node
    for i in output_path:
        if i == '1':
            path.append('G1')
        elif i == '2':
            path.append('G2')
        else: 
            path.append(i)

    # Calculate distance of given path
    for l in range(len(path)-1):
        # source = path[l]
        # target = path[l+1]
        for g in range(len(gn)):
            if gn[g][0] == path[l] and gn[g][1]== path[l+1]:
                path_weight = path_weight + int(gn[g][2])
    
    # Restore path string just in case
    output_path = output_path.replace('1','G1').replace('2','G2')
    return path_weight
    

# return adjacent nodes as a list
def find_neighbors(current_node, gn):
    possible_next_nodes = []
    for x in range(len(gn)):
        if gn[x][0]==current_node:
            possible_next_nodes.append([gn[x][1],int(gn[x][2])])
    return possible_next_nodes




#a* f(n) = h(n)+g(n)
def a_star(current_node, hn, gn):
    distance_queue = PriorityQueue()
    output_path = ''
    current_path = current_node
    current_distance = 0
    distance_queue.put([hn[current_node], current_node, current_path], 0)
    while(distance_queue.empty()==False):
        # Pick a path and the last node with minimum a_star_distance
        get_min = distance_queue.get()
        current_value = get_min[0]
        current_node = get_min[1]
        current_path = get_min[2]

        # Return weight if reaching to goal node and weight is the minimum atm
        if current_node == 'G1' or current_node == 'G2':
            return [current_path,current_value]

        # Get adjacent nodes
        next_nodes = find_neighbors(current_node, gn)
        # Check all possible paths to neighbors and get possible a_star_distance. Store it to priority queue
        for n in range(len(next_nodes)):
            next_node = next_nodes[n][0]
            output_path = current_path + next_node
            path_weight = find_path_weight(output_path, gn)                   # find distance of given path (From S to next_node)
            a_star_distance = path_weight + hn[next_nodes[n][0]]
            distance_queue.put([a_star_distance, next_node, output_path], a_star_distance)
           
    return [current_path,current_value]


# Create solution file
def write_solution_file(filename, optimal_output):
    # create output 'Solutions' folder if not exists
    if not os.path.exists('Solutions'):
        os.makedirs('Solutions')
    output_file = 'Solutions/'+filename.strip('.txt')+'_solution.txt'
    path = 'Solution'
    with open(output_file, 'w') as f:
        f.write(str(optimal_output))  



if __name__ == "__main__":
    args = sys.argv[1:]
    filename = args[0]
    # filename = input("Enter <filename>. Replace '<filename>' to actual filename and do not include '.txt' - ") 
    distance_input_tables = read_table(filename)
    
    # hn
    hn_input_table = find_hn(distance_input_tables)
    # gn
    gn_input_table = find_gn(distance_input_tables)
    # Start node = S
    start_state = 'S'
    # Running a_star algorithm to find optimal path
    optimal_output = a_star(start_state, hn_input_table, gn_input_table)
    print(optimal_output)
    # Write solutions
    write_solution_file(filename, optimal_output)