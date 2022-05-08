import sys
import os
import time

def initial_grid(n):
    board = [[0 for col in range(n)] for row in range(n)]
    return board

# forward checking algorithm
def find_for(board, column, backtracking, num_sol, output_f):
    n = len(board)
    if n <= column:
        num_sol += 1
        f = open(output_f, 'a+')
        solution = ''
        solution += '#' + str(num_sol) + '\n'
        for i in range(len(board)):
            for j in range(len(board[i])):
                solution += ' ' + str(board[i][j]) + ' '
                if j % n == n-1:
                    solution += '\n'
        solution += '\n'
        f.write(solution)
        if num_sol == 2*n:
            return True, backtracking, num_sol
        return False, backtracking, num_sol

    rows = get_rows(board, column)
    for row in rows:
        if not_constraint(board, row, column):
            if forward_checking(board, row, column) == True:
                board[row][column] = 1
                result, backtracking, num_sol = find_for(board, column+1, backtracking, num_sol, output_f)
                if result == True:
                    return True, backtracking, num_sol
                backtracking += 1
                board[row][column] = 0
            else:
                board[row][column] = 0
    return False, backtracking, num_sol

# Forward checking
def forward_checking(board, row, column):
    rows = get_rows(board, column)
    temp = set(rows)
    for r in rows:
        if not_constraint(board, r, column) == False:
            temp.remove(r)

    if len(temp) == 0:
        return False
    else:
        return True


# Maintain Arc Consistency
def find_mac(board, column, backtracking, num_sol, output_f):
    if len(board) == column:
        num_sol += 1
        f = open(output_f, 'a+')
        solution = ''
        solution += '#' + str(num_sol) + '\n'
        for i in range(len(board)):
            for j in range(len(board[i])):
                solution += ' ' + str(board[i][j]) + ' '
                if j % n == n-1:
                    solution += '\n'
        solution += '\n'
        f.write(solution)
        if num_sol == 2*n:
            return True, backtracking, num_sol
        return False, backtracking, num_sol

    rows = get_rows(board, column)
    for row in rows:
        board[row][column] = 1
        unassigned_constraints = get_arc_location(board, column)
        constraint_removed = False
        # Get Arc locations
        for u in unassigned_constraints:
            # MAC
            backtracking += 1
            if not_constraint(board, u[0], u[1]) == False:
                constraint_removed = True
                break
        
        if constraint_removed == False:   
            mac_return, backtracking, num_sol = find_mac(board, column + 1,backtracking, num_sol, output_f)
            if mac_return == True:
                return True, backtracking, num_sol
        
        board[row][column] = 0
    return False, backtracking, num_sol

# Get only neighbors (Arc)
def get_arc_location(board, column):
    result = []
    for row in range(len(board)):
        if column < len(board)-1:
            for col in range(column+1, column+2):
                if board[row][col] == 0 and not_constraint(board, row, col):
                    result.append([row,col])
    return result


################################# COMMON FUNCTIONS FOR BOTH ALGORITHMS. CHECK CONSTRAINTS ###################################
# Get rows without constraint
def get_rows(board, queen):
    rows = []
    for row in range(len(board)):
        if not_constraint(board, row, queen) == True:
            rows.append(row)
    return rows



# Check constraints - true when not constraint, false when constraint
def not_constraint(board, row, column):
    # no constraint - should be all true for row, column, diagonal
    return check_row(board, row) and check_column(board, column) and check_diagonal(board,row,column)

def check_row(board, row):
    for col in range(len(board)):
        if board[row][col] == 1:
            return False
    return True

def check_column(board, column):
    for row in range(len(board)):
        if board[row][column] == 1:
            return False
    return True

def check_diagonal(board, row, column):
    return diagonal_up(board, row ,column) and diagonal_down(board, row, column)

# Checking up direction of diagonal
def diagonal_up(board, row, column):
    r = row
    c = column
    while c >= 0 and r >= 0:
        if board[r][c] == 1:
            return False
        c -= 1
        r -= 1
    return True

# Checking down direction of diagonal
def diagonal_down(board, row, column):
    r = row
    c = column
    while c >= 0 and r  < len(board):
        if board[r][c] == 1:
            return False
        c -= 1
        r += 1
    return True




# MAIN 
def lets_start(algo_type, n):
    board = initial_grid(n)
    
    # Create solution folder if not exist
    directory = "Solutions/" 
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Delete output file if exists
    output_file = "Solutions/" +algo_type+'_' + str(n) + '.txt'
    if os.path.exists(output_file):
        os.remove(output_file)


    backtracking = 0
    num_sol = 0

    # Maintain arc consistency
    if algo_type == 'MAC':
        # parse initial board, initial queen's location (column 0), # of backtracking
        result, backtracking, num_sol = find_mac(board, 0, backtracking, num_sol, output_file)

        # Formatting output file
        prepend = 'MAC \n\n' + 'Solutions : ' + str(num_sol) +'\n\nBacktracks : ' + str(backtracking) + '\n \n'
        with open(output_file, 'r+') as s:
            n_queen_solutions = s.read()
            s.seek(0)
            s.write(prepend + n_queen_solutions)   
        print('time: ', time.time() - start_time)
    # Forward checking 
    elif algo_type == 'FOR':
        # parse initial board, initial queen's location (column 0), # of backtracking 
        result, backtracking, num_sol = find_for(board, 0, backtracking, num_sol, output_file)

        # Formatting output file
        prepend = 'FORWARD CHECKING \n\n' + 'Solutions : ' + str(num_sol) +'\n\nBacktracks : ' + str(backtracking) + '\n \n'
        with open(output_file, 'r+') as s:
            n_queen_solutions = s.read()
            s.seek(0)
            s.write(prepend + n_queen_solutions)  
        print('time: ', time.time() - start_time)

if __name__ == "__main__":
    args = sys.argv[1:]
    algo_type = args[0].upper()
    start_time = time.time()
    n = int(args[1])
    if n < 4:
        print('No solution exists')
    else:
        lets_start(algo_type, n)
        
    