import copy
import random
from SudokuGeneratorWithoutMath import *

'''
Backtracking from https://www.geeksforgeeks.org/dsa/sudoku-backtracking-7/

EasySolve currently has
LastSlot
LastDigit

Pointed to make easier solutions

Now need hidden pair & naked pair 

'''

def EasySolve(grid):
    '''
    Idee:
    while counter < 81:
        for all digits
            check easy solve strats
    return grid
    '''
    counter = 0
    possible_set = CheckPossibleSet(grid)

    summe_old = 0
    solving_grid = copy.deepcopy(grid)

    while counter < 81:
        found, row, column, digit = LastPossibleSpot(solving_grid, possible_set)
        if found:
            solving_grid[row][column] = digit
            possible_set = CheckPossibleSet(solving_grid)

        else:
            #print(possible_set)
            found, row, column, digit = LastDigit(solving_grid, possible_set)
            if found:

                solving_grid[row][column] = digit
                possible_set = CheckPossibleSet(solving_grid)




        summe_new = sum(solving_grid[i][j] for i in range(9) for j in range(9))
        if summe_new == summe_old:
                break
        else:
            summe_old = summe_new
        counter +=1
        if sum(solving_grid[i][j] for i in range(9) for j in range(9)) == 405:
            break
    return solving_grid

def EasySolvePointed(grid):
    '''
    Idee:
    while counter < 81:
        for all digits
            check easy solve strats
    return grid
    '''
    counter = 0
    possible_set = CheckPossibleSet(grid)
    possible_set = Pointed(possible_set)
    #print(Pointed(possible_set))
    summe_old = 0
    solving_grid = copy.deepcopy(grid)

    while counter < 81:
        found, row, column, digit = LastPossibleSpot(solving_grid, possible_set)
        if found:
            solving_grid[row][column] = digit
            possible_set = CheckPossibleSet(solving_grid)
            possible_set = Pointed(possible_set)
        else:
            #print(possible_set)
            found, row, column, digit = LastDigit(solving_grid, possible_set)
            if found:

                solving_grid[row][column] = digit
                possible_set = CheckPossibleSet(solving_grid)
                possible_set = Pointed(possible_set)



        summe_new = sum(solving_grid[i][j] for i in range(9) for j in range(9))
        if summe_new == summe_old:
                break
        else:
            summe_old = summe_new
        counter +=1
        if sum(solving_grid[i][j] for i in range(9) for j in range(9)) == 405:
            break
    return solving_grid

def LastPossibleSpot(grid, possible_set):
    #possible_set = CheckPossibleSet(grid)
    for digit in range(1,10,1):
        #CHECK EVERY BOX
        for box in range(9):
            start_row = 3*(box % 3)
            start_column = 3*(box // 3)
            counter = 0
            for i in range(3):
                for j in range(3):
                    if digit in possible_set[start_row+i][start_column+j]:
                        counter += 1
                        row = start_row+i
                        column = start_column+j
            if counter ==1:
                return (True, row, column, digit)

        #CHECK EVERY ROW
        for i in range(9):
            counter = 0
            for j in range(9):
                if digit in possible_set[i][j]:
                    counter += 1

                    row = i
                    column = j
            if counter ==1:
                return (True, row, column, digit)

        #CHECK EVERY COLUMN
        for j in range(9):
            counter = 0
            for i in range(9):
                if digit in possible_set[i][j]:
                    counter += 1
                    row = i
                    column = j
            if counter ==1:
                return (True, row, column, digit)


    return False, None, None, None

def LastDigit(grid, possible_set):
    #possible_set = CheckPossibleSet(grid)
    for digit in range(1,10,1):
        for i in range(9):
            for j in range(9):
                if digit in possible_set[i][j] and len(possible_set[i][j])==1:
                    return (True, i, j, digit)
    return (False, None, None, None)

def CheckPossibleSet(grid):
    possible_set_grid = [[set() for i in range(9)] for j in range(9)]
    for digit in range(1,10,1):
        for i in range(9):
            for j in range(9):
                if grid[i][j] ==0 and isValid(grid, i, j, digit):
                    possible_set_grid[i][j].add(digit)
#                if grid[i][j] != 0:
#                    possible_set_grid[i][j] = grid[i][j]
    return possible_set_grid

def Pointed(possible_set_grid):
    #CHECK EACH BOX FOR A POINTED PAIR/TRIPLE
    #IF FOUND, ELIMINATE OTHER CANDIDATES FROM ROW/COLUMN

    for digit in range(1,10,1):
        for box in range(9):
            counter_row = [0,0,0]
            counter_column = [0,0,0]
            start_row = 3 * (box % 3)
            start_column = 3 * (box // 3)
            for i in range(3):
                for j in range(3):
                    if digit in possible_set_grid[start_row+i][start_column+j]:
                        counter_row[i] =1
                        counter_column[j] =1


            if sum(counter_row) ==1:
                add_row = counter_row.index(1)
                row = start_row + add_row
                columns = [start_column+i for i in range(3)]
                for i in range(9):
                    if not i in columns:
                        if digit in possible_set_grid[row][i]:

                            possible_set_grid[row][i].remove(digit)


            if sum(counter_column) ==1:
                add_column = counter_column.index(1)
                column = start_column + add_column
                rows = [start_row+i for i in range(3)]
                for i in range(9):
                    if not i in rows:
                        if digit in possible_set_grid[i][column]:

                            possible_set_grid[i][column].remove(digit)


    return possible_set_grid



def CheckOneSlot(grid):
    solving_grid = copy.deepcopy(grid)
    possible_set = CheckPossibleSet(solving_grid)
    found, row, column, digit = LastPossibleSpot(solving_grid, possible_set)
    pointed = False
    if found:
        return found, row, column, digit, 'Last Spot', pointed
    else:
        found, row, column, digit = LastDigit(solving_grid, possible_set)
        if found:
            return found, row, column, digit, 'Last Digit', pointed
        else:
            possible_set = Pointed(possible_set)
            pointed = True
            found, row, column, digit = LastPossibleSpot(solving_grid, possible_set)
            if found:
                return found, row, column, digit, 'Last Spot', pointed
            else:
                found, row, column, digit = LastDigit(solving_grid, possible_set)
                if found:
                    return found, row, column, digit, 'Last Digit', pointed
                else:
                    return found, None, None, None, 'No Solution', pointed




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




'''
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
'''
def GenerateFilledGrid():
    random_first_row = [i + 1 for i in range(9)]
    random.shuffle(random_first_row)
    random_grid = [[0 for i in range(9)] for j in range(9)]
    random_grid[0] = random_first_row
    grid, counter = SudokuGrid(random_grid)
    return grid


def GenerateSudoku(number_of_digits):
    # Go through randomized list of the 81 digits,

    temp = list(range(81))
    random.shuffle(temp)

    grid = GenerateFilledGrid()

    complete_grid_swapped = SwapDigitsRandom(grid)
    complete_grid = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            complete_grid[i][j] = complete_grid_swapped[i][j]

    counter = 0

    for i in range(81):
        random_row = temp[i] // 9
        random_column = temp[i] % 9


        if complete_grid_swapped[random_row][random_column] != 0:
            number = complete_grid_swapped[random_row][random_column]

            complete_grid_swapped[random_row][random_column] = 0
            solution, counter_solutions = SudokuGrid(complete_grid_swapped)


            if counter_solutions >1:
                complete_grid_swapped[random_row][random_column] = number
            elif counter_solutions == 1:
                counter += 1
                if counter == (81 - number_of_digits):
                    break
    return complete_grid_swapped, complete_grid

def SwapDigitsRandom(grid):
    temp = list(range(9))
    random.shuffle(temp)

    swappedGrid = [[0 for i in range(9)] for j in range(9)]

    for i in range(9):
        for j in range(9):
            old_digit = grid[i][j]
            new_digit = temp[old_digit-1]
            swappedGrid[i][j] = new_digit+1
    return swappedGrid

def GenerateDailySudoku():
    current_day = datetime.datetime.today().day
    current_month = datetime.datetime.today().month
    current_year = datetime.datetime.today().year

    random_seed = current_day + 40 * current_month + 1000 * current_year

    random.seed(random_seed)
    rand_int = random.randint(1, 12)
    rand_amount_digits = 22 + rand_int

    grid, complete_grid = GenerateSudoku(rand_amount_digits)
    return grid, complete_grid

'''
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
'''






if __name__ == '__main__':
    global first_solution
    grid2 = [
        [0, 5, 0, 9, 0, 0, 1, 6, 0],
        [9, 0, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 4, 0, 0, 0, 0, 0, 5],

        [7, 0, 3, 4, 0, 0, 0, 5, 1],
        [0, 2, 0, 0, 5, 7, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 7, 0, 0],

        [8, 0, 0, 0, 4, 0, 0, 3, 0],
        [2, 0, 0, 3, 0, 0, 0, 1, 8],
        [0, 0, 0, 1, 8, 0, 5, 0, 2]]

    grid = [
        [1,0,5,0,6,4,0,7,3],
        [4,9,0,0,0,0,0,1,0],
        [0,7,3,0,0,1,6,0,2],
        [5,8,4,6,0,2,0,0,0],
        [0,0,9,0,8,0,4,0,0],
        [2,0,0,4,3,9,5,8,6],
        [0,0,8,3,2,0,1,6,4],
        [7,4,0,9,5,0,2,3,0],
        [3,6,2,1,4,8,7,5,0]

    ]

    solution, counter = SudokuGrid(grid)

    grid, complete_grid = GenerateSudoku(40)
    test = CheckOneSlot(grid)
    print(grid)
    print(test)



