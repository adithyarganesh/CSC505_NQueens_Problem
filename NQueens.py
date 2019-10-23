import sys
import time


# Creating a class QueenGraph to store each element as an object that contains its respective neighbours, constraints
# and domains
class QueenGraph:
    def __init__(self, domains, constraints, variables, neighbors):
        self.constraints = constraints
        self.domains = domains
        self.variables = variables
        self.neighbors = neighbors


# Creating the initial chessboard for a given dimension and initializing it to zero
def initialize_chess_board(n):
    board = []
    for _ in range(n):
        twod_board = []
        for i in range(n):
            twod_board.append(0)
        board.append(twod_board)
    return board


# To check if there are any queens placed in the same row
def horizontal(loc, matrix):
    index = loc[0]
    for _ in matrix[index]:
        if _ == 100:
            return 1
    return 0


# To check if there are any queens placed in the upper diagonal
def diagonal1(loc, matrix):
    x = loc[0]
    y = loc[1]
    n = len(matrix[0])
    while x >=0 and y >= 0:
        if matrix[x][y] == 100:
            return 1
        x -= 1
        y -= 1
    x = loc[0] + 1
    y = loc[1] + 1
    while x < n and y < n:
        if matrix[x][y] == 100:
            return 1
        x += 1
        y += 1
    return 0


# To check if there are any queens placed in the lower diagonal
def diagonal2(loc, matrix):
    x = loc[0]
    y = loc[1]
    n = len(matrix[0])
    while x < n and y >= 0:
        if matrix[x][y] == 100:
            return 1
        x += 1
        y -= 1
    x = loc[0]
    y = loc[1]
    while x >= 0 and y < n:
        if matrix[x][y] == 100:
            return 1
        x -= 1
        y += 1
    return 0


# Checking all constraints before placing queen at (loc)
def add_queen(loc, matrix):
    output = 0
    output += horizontal(loc, matrix)
    output += diagonal1(loc, matrix)
    output += diagonal2(loc, matrix)
    if output == 0:
        return True
    else:
        return False


# Keep track of all the spaces where queens cannot be placed by initializing with row number for forward checking
# Removing the initialized numbers while backtracking
def forward_backtrack(loc, board, value):
    row = loc[0]
    col = loc[1]
    n = len(board[0])
    dic = {0: row+1}
    new_value = 0
    if value in dic.keys():
        new_value = dic[value]
    # Setting cell values dynamically depending on forward/backtracking
    for i, j in zip(range(row - 1, -1, -1), range(col + 1, n, 1)):
        if board[i][j] == value:
            board[i][j] = new_value

    for i, j in zip(range(row + 1, n, 1), range(col + 1, n, 1)):
        if board[i][j] == value:
            board[i][j] = new_value

    for j in range(col + 1, n, 1):
        if board[row][j] == value:
            board[row][j] = new_value
    # To check if any column is free
    temp = board[:]
    temp = map(list, zip(*temp))
    for xx in temp:
        if 0 not in xx and 100 not in xx:
            return False
    return True


# Storing the columns of chess board in human readable form in RFile
def get_column(dlist):
    arr = []
    for i in dlist:
        if i != 100:
            arr.append('-')
        else:
            arr.append('Q')
    return str(arr).replace('\'', '').replace(',', '')


# Algorithm for forward checking
def for_checking(board, col, steps, solns, file):
    n = len(board[0])
    if col >= n:
        f = open(file, "a+")
        f.write("\nSolution: %d\n" % int(solns+1))
        for _ in board:
            f.write("%s\r" % get_column(_))
        solns += 1
        if solns == 2 * n:
            return True, steps, solns
        return False, steps, solns

    for row in range(n):
        pos = (row, col)
        if add_queen(pos, board):
            if forward_backtrack(pos, board, 0):
                board[row][col] = 100
                rec, steps, solns = for_checking(board, col + 1, steps, solns, file)
                if rec:
                    return rec, steps, solns
                steps += 1
            else:
                board[row][col] = 0
                forward_backtrack(pos, board, row + 1)
            board[row][col] = 0
            forward_backtrack(pos, board, row+1)
    return False, steps, solns


# Algorithm to determine queen position from constraints and domains developed
def ac3(domain, neighbors, constraints, col):
    curr = neighbors[0]
    if col+1 < len(domain.keys()):
        queue = list(constraints[(col, col+1)])
        while queue:
            val = queue[0]
            queue = queue[1:]
            col_1 = val[0]
            col_2 = val[1]
            new_domain,  curr = revise(domain, constraints, col_1, col_2, col + 1)
            if new_domain[0]:
                domain[curr] = new_domain[0]
                return True, domain, constraints
        domain[curr] = []
    return False, domain, constraints


# Obtaining the new set of domains and constraints and revising the domain of the column
def revise(domain, constraints, x_coordinate, y_coordinate, current_col):
    column_constraints = []
    for col in range(current_col, 0, -1):
        constraint_values = constraints[(col - 1, current_col)]
        check = domain[col - 1][0]
        col_constraints = []
        for (i, j) in constraint_values:
            if i == check:
                col_constraints.append(j)
        column_constraints.append(col_constraints)
    dom_new = [list(set.intersection(*map(set, column_constraints)))]
    if not dom_new:
        dom_new = [[]]
    return dom_new, current_col


# Getting user readable representation
def get_board(domain):
    board = initialize_chess_board(len(domain.keys()))
    for key, value in domain.items():
        board[key][value[0]] = 100
    return board


# Defining the start case for running the Arc Consistancy algorithm
def mac(queenGraph, domain, neighbors, constraints, column_index, steps, solns, file):
    size = len(domain.keys())
    # When all Queens are placed
    if column_index + 1 > size:
        return True, steps, solns
    for _ in domain[column_index]:
        # Place the queen in the current position
        check, domain_new, constraints_new = ac3(domain.copy(), neighbors.copy(), constraints.copy(), column_index)
        # We pass the copy of the variable because we can determine whether while backtracking, we restore the old values or use the new ones.
        if check:
            domain = domain_new.copy()
            constraints = constraints_new.copy()
            # Checking if the domain has only single value for each key
            if len(domain[size - 1]) == 1:
                solns += 1
                board = get_board(domain)
                f = open(file, "a+")
                f.write("\nSolution: %d\n" % int(solns))
                for _ in board:
                    f.write("%s\r" % get_column(_))
                if solns == 2 * size:
                    print("Number of solutions found: ", solns)
                    print("Real time taken: %s secs" % (time.time() - start_time))
                    print("Number of Backtracking steps: ", steps)
                    exit(1)
                break
            rec, steps, solns = mac(queenGraph, domain, neighbors, constraints, column_index + 1, steps, solns, file)
            steps += 1
        domain[column_index] = domain[column_index][1:]
        if not domain[column_index]:
            return False, steps, solns
    return True, steps, solns


# Generating all the free chessboard locations where the queen is safe
def get_value_pairs(num, diff):
    temp = []
    for val in range(num):
        for x in range(num):
            if val not in (x - diff, x, x + diff):
                temp.append((val, x))
    return temp


# Generating the CFile by creating objects for Variables, Domains, Neighbors and Constraints in a given board size
def get_constraints(num, g):
    constraint_keys = {}
    domains = {}
    variables = []
    indices = []
    neighbors = {}
    QGraph = QueenGraph(constraint_keys, domains, variables, neighbors)
    for i in range(num):
        indices.append(i)
    for i in range(num):
        QGraph.domains[i] = indices
        domains[i] = indices
    for _ in range(num):
        QGraph.variables.append(str('Q'+str(_)))
        variables.append(str('Q' + str(_)))
    for i in range(num):
        temp = indices[:]
        temp.remove(i)
        neighbors[i] = temp
        QGraph.neighbors[i] = temp
    g.write("Variables:%s\r" % variables)
    g.write("Domains:%s\r" % domains)
    g.write("Neighbors:%s\r" % neighbors)
    g.write("Constraints: There are %sc2 constraints involved\r" % num)
    # Generating all possible locations where two queens can be placed - Constraint generation
    for i in range(num-1):
        for j in range(i+1, num):
            if (j, i) not in constraint_keys.keys():
                constraint_keys[(i,j)] = get_value_pairs(num, i-j)
                g.write("R(Q%s\r" % str(str(i)+", Q" + str(j) + ") = %s" % str(constraint_keys[(i, j)])))
    g.write("where R(Qi, Qj) represents the rows 1 and j and the corresponding tuples determine the locations where the Queen can be placed")
    g.close()
    return QGraph, variables, domains, neighbors, constraint_keys


#Parsing the system arguments and running the respective algorithms for the N-Queens problem
def main():
    ALG = sys.argv[1]
    n = int(sys.argv[2])
    CFile = sys.argv[3]
    RFile = sys.argv[4]
    open(RFile, 'w').close()
    open(CFile, 'w').close()
    steps = 0
    solns = 0
    board = initialize_chess_board(n)
    g = open(CFile, "a+")
    QGraph, variables, domains, neighbors, constraint_keys = get_constraints(n, g)
    if ALG == "FOR":
        rec, steps, solns = for_checking(board, 0, steps, solns, RFile)
    elif ALG == "MAC":
        rec, steps, solns = mac(QGraph, domains, neighbors, constraint_keys, 0, steps, solns,  RFile)
    print("Number of solutions found: ", solns)
    print("Real time taken: %s secs" % (time.time() - start_time))
    print("Number of Backtracking steps: ", steps)


if __name__ == "__main__":
    start_time = time.time()
    main()
