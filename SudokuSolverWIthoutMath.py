import copy

'''
Backtracking from https://www.geeksforgeeks.org/dsa/sudoku-backtracking-7/

'''

def isValid(grid, row, col, digit):
    for i in range(9):
        if grid[i][col] == digit:
            return False
    for j in range(9):
        if grid[row][j] == digit:
            return False
    #STARTING COORDINATES IN BOX
    start_row = row - (row % 3)
    start_col = col - (col % 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == digit:
                return False
    return True

def SolveGrid(grid, row, col, solutions, first_solution):
    if row == 8 and col == 9:
        if solutions == 0:
            first_solution.append(copy.deepcopy(grid))
        return solutions +1
    if col == 9:
        return SolveGrid(grid, row +1, 0, solutions, first_solution)
    if grid[row][col] != 0:
        return SolveGrid(grid, row, col+1, solutions, first_solution)

    for digit in range(1,10):
        if isValid(grid, row, col, digit):
            grid[row][col] = digit
            # CHECK IF SUDOKU HAS SOLUTION WITH THAT DIGIT
            solutions = SolveGrid(grid, row, col+1, solutions, first_solution)
            if solutions >1:
                return solutions

            # IF IT DOESNT, GET RID OF DIGIT AGAIN
            grid[row][col] = 0
    return solutions


def SudokuGrid(grid):
    global first_solution
    first_solution = []
    grid2 = copy.deepcopy(grid)
    solutions = SolveGrid(grid2, 0, 0, 0, first_solution)


    return (first_solution[0], solutions) if first_solution else (None, solutions)




if __name__ == '__main__':
    global first_solution
    grid = [
        [0, 5, 0, 9, 0, 0, 1, 6, 0],
        [9, 0, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 4, 0, 0, 0, 0, 0, 5],

        [7, 0, 3, 4, 0, 0, 0, 5, 1],
        [0, 2, 0, 0, 5, 7, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 7, 0, 0],

        [8, 0, 0, 0, 4, 0, 0, 3, 0],
        [2, 0, 0, 3, 0, 0, 0, 1, 8],
        [0, 0, 0, 1, 8, 0, 5, 0, 2]]

    solution, counter = SudokuGrid(grid)


    print(solution, counter)
