board = [
    [0,0,9,0,4,0,0,0,0],
    [0,0,0,0,0,5,3,1,0],
    [0,6,1,0,0,8,0,5,0],
    [0,0,5,4,0,0,2,0,3],
    [0,1,0,0,0,7,0,0,8],
    [0,8,0,0,0,0,7,6,0],
    [3,0,6,0,1,9,4,0,0],
    [7,0,0,0,0,0,0,0,0],
    [0,0,4,0,5,0,6,2,7]

]

# Solver.py
def solve(su):
    
    """ Solves the sudoku board using backtracking """

    find = find_empty(su)
    if find:
        row, col = find
    else:
        return True

    for i in range(1,10):
        if valid(su, (row, col), i):
            su[row][col] = i

            if solve(su):
                return True

            su[row][col] = 0

    return False


def valid(su, pos, num):
    
    """ Returns if the attempted move is valid """

    # Check row

    for i in range(0, len(su)):
        if su[pos[0]][i] == num and pos[1] != i:
            return False

    # Check Column 

    for i in range(0, len(su)):
        if su[i][pos[1]] == num and pos[1] != i:
            return False

    # Check box

    box_x = pos[1]//3
    box_y = pos[0]//3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if su[i][j] == num and (i,j) != pos:
                return False

    return True


def find_empty(su):
    
    """ finds an empty space in the board """

    for i in range(len(su)):
        for j in range(len(su[0])):
            if su[i][j] == 0:
                return (i, j)

    return None


def print_board(su):

    """ prints the board """

    for i in range(len(su)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(su[0])):
            if j % 3 == 0 and j != 0:
                print(" | ",end="")

            if j == 8:
                print(su[i][j], end="\n")
            else:
                print(str(su[i][j]) + " ", end="")

print_board(board)
solve(board)
print('_______________________')
print('')
print_board(board)
