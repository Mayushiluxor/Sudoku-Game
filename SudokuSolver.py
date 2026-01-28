import copy
import random
from SudokuGenerator import *

'''
Backtracking from https://www.geeksforgeeks.org/dsa/sudoku-backtracking-7/

EasySolve currently has
LastSlot
LastDigit

Pointed to make easier solutions
naked pair -> check for all spots that only 2 digits can be -> check for pairs

Now need hidden pair & naked pair 
hidden pair -> check for all digits that can be in exactly 2 spots -> check for pairs
hidden pair -> any possiblity if there are 3 pairs? check theory

check if pointed works intended now

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
        found, row, column, digit, message = LastPossibleSpot(solving_grid, possible_set)
        if found:
            solving_grid[row][column] = digit
            possible_set = CheckPossibleSet(solving_grid)

        else:
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
    possible_set, deleted = Pointed(possible_set)
    summe_old = 0
    solving_grid = copy.deepcopy(grid)

    while counter < 81:
        found, row, column, digit, message = LastPossibleSpot(solving_grid, possible_set)
        if found:
            solving_grid[row][column] = digit
            possible_set = CheckPossibleSet(solving_grid)
            possible_set, deleted = Pointed(possible_set)
        else:
            found, row, column, digit = LastDigit(solving_grid, possible_set)
            if found:

                solving_grid[row][column] = digit
                possible_set = CheckPossibleSet(solving_grid)
                possible_set, deleted = Pointed(possible_set)



        summe_new = sum(solving_grid[i][j] for i in range(9) for j in range(9))
        if summe_new == summe_old:
                break
        else:
            summe_old = summe_new
        counter +=1
        if sum(solving_grid[i][j] for i in range(9) for j in range(9)) == 405:
            break
    return solving_grid

def EasySolvePointedAndPair(grid):
    '''
    Idee:
    while counter < 81:
        for all digits
            check easy solve strats
    return grid
    '''
    counter = 0
    possible_set = CheckPossibleSet(grid)
    deleted = True
    while deleted == True:
        possible_set, deleted1 = Pointed(possible_set)
        possible_set, deleted2 = naked_pair(possible_set)
        possible_set, deleted3 = hidden_pair(possible_set)
        if deleted1 or deleted2 or deleted3:
            deleted = True
        else:
            deleted = False

    summe_old = 0
    solving_grid = copy.deepcopy(grid)

    while counter < 81:
        found, row, column, digit, message = LastPossibleSpot(solving_grid, possible_set)
        found_this_iteration = False
        if found:
            found_this_iteration = True

            solving_grid[row][column] = digit
            possible_set = CheckPossibleSet(solving_grid)
            deleted = True
            while deleted == True:
                possible_set, deleted1 = Pointed(possible_set)
                possible_set, deleted2 = naked_pair(possible_set)
                possible_set, deleted3 = hidden_pair(possible_set)
                if deleted1 or deleted2 or deleted3:
                    deleted = True
                else:
                    deleted = False
        else:
            found, row, column, digit = LastDigit(solving_grid, possible_set)
            if found:
                found_this_iteration = True

                solving_grid[row][column] = digit
                possible_set = CheckPossibleSet(solving_grid)
                deleted = True
                while deleted == True:
                    possible_set, deleted1 = Pointed(possible_set)
                    possible_set, deleted2 = naked_pair(possible_set)
                    possible_set, deleted3 = hidden_pair(possible_set)
                    if deleted1 or deleted2 or deleted3:
                        deleted = True
                    else:
                        deleted = False

        if not found_this_iteration:
            break
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
                return (True, row, column, digit, 'Box')

        #CHECK EVERY ROW
        for i in range(9):
            counter = 0
            for j in range(9):
                if digit in possible_set[i][j]:
                    counter += 1

                    row = i
                    column = j
            if counter ==1:
                return (True, row, column, digit, 'Column')

        #CHECK EVERY COLUMN
        for j in range(9):
            counter = 0
            for i in range(9):
                if digit in possible_set[i][j]:
                    counter += 1
                    row = i
                    column = j
            if counter ==1:
                return (True, row, column, digit, 'Row')


    return False, None, None, None, None

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

    deleted = False
    for digit in range(1,10,1):
        for box in range(9):
            counter_row = [0,0,0]
            counter_column = [0,0,0]
            actual_counter_row = [0,0,0]
            actual_counter_column = [0,0,0]
            start_row = 3 * (box % 3)
            start_column = 3 * (box // 3)
            for i in range(3):
                for j in range(3):
                    if digit in possible_set_grid[start_row+i][start_column+j]:
                        counter_row[i] =1
                        counter_column[j] =1
                        actual_counter_row[i] +=1
                        actual_counter_column[j] +=1


            if sum(counter_row) ==1 and sum(actual_counter_row) >=2:
                add_row = counter_row.index(1)
                row = start_row + add_row
                columns = [start_column+i for i in range(3)]
                for i in range(9):
                    if not i in columns:
                        if digit in possible_set_grid[row][i]:
                            deleted = True
                            possible_set_grid[row][i].remove(digit)


            if sum(counter_column) ==1 and sum(actual_counter_column) >=2:
                add_column = counter_column.index(1)
                column = start_column + add_column
                rows = [start_row+i for i in range(3)]
                for i in range(9):
                    if not i in rows:
                        if digit in possible_set_grid[i][column]:
                            deleted = True
                            possible_set_grid[i][column].remove(digit)


    return possible_set_grid, deleted

def naked_pair(possible_set_grid):
    '''
    if only 2 numbers can be in 2 spots in a box/row/column, these numbers can be eliminated from any other spot in the box/row/column

    idea: naked pair -> check for all spots that only 2 digits can be -> check for pairs
    '''
    #check in box
    found = False
    deleted = False
    for box in range(9):
        found_pair = []
        pairs_box = []
        start_row = 3 * (box % 3)
        start_column = 3 * (box // 3)
        for row in range(3):
            for column in range(3):
                if len(possible_set_grid[start_row+row][start_column+column])==2:
                    pairs_box.append((possible_set_grid[start_row+row][start_column+column], start_row+row, start_column+column))
        for i in range(len(pairs_box)):
            for j in range(i, len(pairs_box), 1):
                if i != j:
                    if pairs_box[i][0] == pairs_box[j][0]:
                        found_pair.append((pairs_box[i][0],pairs_box[i][1],pairs_box[i][2], pairs_box[j][1], pairs_box[j][2]))
                        found = True
        if found:
            for pair in found_pair:
                col_row_pair = ((pair[1], pair[2]), (pair[3], pair[4]))
                digits = pair[0]
                for i in range(3):
                    for j in range(3):
                        if (start_row+i,start_column+j) not in col_row_pair:
                            for digit in digits:
                                if digit in possible_set_grid[start_row+i][start_column+j]:
                                    deleted = True
                                    possible_set_grid[start_row+i][start_column+j].remove(digit)
            found = False


    #check in row
    for row in range(9):
        found_pair = []
        pairs_row = []
        for column in range(9):
            if len(possible_set_grid[row][column]) == 2:
                pairs_row.append((possible_set_grid[row][column], row, column))
        for i in range(len(pairs_row)):
            for j in range(i, len(pairs_row),1):
                if i!=j:
                    if pairs_row[i][0] == pairs_row[j][0]:
                        found_pair.append((pairs_row[i][0],pairs_row[i][1],pairs_row[i][2], pairs_row[j][1], pairs_row[j][2]))
                        found = True
        if found:

            for pair in found_pair:
                columns = (pair[2], pair[4])
                digits = pair[0]
                for i in range(9):
                    if i not in columns:
                        for digit in digits:
                            if digit in possible_set_grid[row][i]:
                                deleted = True
                                possible_set_grid[row][i].remove(digit)


            found = False
    #check in column
    for column in range(9):
        found_pair = []
        pairs_column = []
        for row in range(9):
            if len(possible_set_grid[row][column]) == 2:
                pairs_column.append((possible_set_grid[row][column], row, column))
        for i in range(len(pairs_column)):
            for j in range(i, len(pairs_column),1):
                if i != j:

                    if pairs_column[i][0] == pairs_column[j][0]:
                        found_pair.append((pairs_column[i][0], pairs_column[i][1], pairs_column[i][2], pairs_column[j][1], pairs_column[j][2]))
                        found = True
        if found:
            for pair in found_pair:
                rows = (pair[1], pair[3])
                digits = pair[0]
                for i in range(9):
                    if i not in rows:
                        for digit in digits:
                            if digit in possible_set_grid[i][column]:
                                deleted = True
                                possible_set_grid[i][column].remove(digit)


            found = False



    return possible_set_grid, deleted

def hidden_pair(possible_set_grid):
    '''
    If 2 numbers can only be in 2 spots, any other candidate in these 2 spots can be eliminated

    idea: hidden pair -> check for all digits that can be in exactly 2 spots -> check for pairs
    '''
    #check box

    deleted = False

    for box in range(9):
        counter_numbers_box = [[0] for i in range(9)]
        start_row = 3 * (box % 3)
        start_column = 3 * (box // 3)
        for row_box in range(3):
            for column_box in range(3):
                for digit in possible_set_grid[start_row+row_box][start_column+column_box]:
                    counter_numbers_box[digit-1][0] +=1
                    counter_numbers_box[digit-1].append([row_box,column_box])

        for i in range(9):
            if counter_numbers_box[i][0] == 2:
                for j in range(i+1, 9,1 ):
                    if counter_numbers_box[j][0] == 2 and counter_numbers_box[i][1] == counter_numbers_box[j][1] and counter_numbers_box[i][2] == counter_numbers_box[j][2]:
                        first_pair = counter_numbers_box[i][1]
                        second_pair = counter_numbers_box[i][2]
                        for digits in range(9):
                            if digits != i and digits != j and digits+1 in possible_set_grid[start_row+first_pair[0]][start_column+first_pair[1]]:
                                possible_set_grid[start_row+first_pair[0]][start_column+first_pair[1]].remove(digits+1)
                                deleted = True
                            if digits != i and digits != j and digits+1 in possible_set_grid[start_row+second_pair[0]][start_column+second_pair[1]]:
                                possible_set_grid[start_row+second_pair[0]][start_column+second_pair[1]].remove(digits+1)
                                deleted = True


    #check row
    for row in range(9):
        counter_numbers_row = [ [0] for i in range(9)]
        for column in range(9):

            for digit in possible_set_grid[row][column]:

                counter_numbers_row[digit-1][0] += 1
                counter_numbers_row[digit-1].append(column)

        for i in range(9):
            if counter_numbers_row[i][0] == 2:
                for j in range(i+1, 9, 1):
                    if counter_numbers_row[j][0] == 2 and counter_numbers_row[i][1] == counter_numbers_row[j][1] and counter_numbers_row[i][2] == counter_numbers_row[j][2]:

                        for digits in range(9):
                            if digits != i and digits != j and (digits+1) in possible_set_grid[row][counter_numbers_row[i][1]]:
                                possible_set_grid[row][counter_numbers_row[i][1]].remove(digits+1)
                                deleted = True
                            if digits != i and digits != j and (digits+1) in possible_set_grid[row][counter_numbers_row[i][2]]:
                                possible_set_grid[row][counter_numbers_row[i][2]].remove(digits+1)
                                deleted = True

    #check column
    for column in range(9):
        counter_numbers_column = [ [0] for i in range(9)]
        for row in range(9):
            for digit in possible_set_grid[row][column]:
                counter_numbers_column[digit-1][0] += 1
                counter_numbers_column[digit-1].append(row)
        for i in range(9):
            if counter_numbers_column[i][0] == 2:
                for j in range(i+1, 9, 1):
                    if counter_numbers_column[j][0] == 2 and counter_numbers_column[i][1] == counter_numbers_column[j][1] and counter_numbers_column[i][2] == counter_numbers_column[j][2]:

                        for digits in range(9):
                            if digits != i and digits != j and (digits+1) in possible_set_grid[counter_numbers_column[i][1]][column]:
                                possible_set_grid[counter_numbers_column[i][1]][column].remove(digits+1)
                                deleted = True

                            if digits != i and digits != j and (digits+1) in possible_set_grid[counter_numbers_column[i][2]][column]:
                                possible_set_grid[counter_numbers_column[i][2]][column].remove(digits+1)
                                deleted = True

    return possible_set_grid, deleted



def CheckOneSlot(grid):
    solving_grid = copy.deepcopy(grid)
    possible_set = CheckPossibleSet(solving_grid)
    found, row, column, digit, message = LastPossibleSpot(solving_grid, possible_set)

    if found:
        which_row_col_box = 'Last Spot ' + message
        return found, row, column, digit, which_row_col_box
    else:
        found, row, column, digit = LastDigit(solving_grid, possible_set)
        if found:
            return found, row, column, digit, 'Last Digit'
        else:
            deleted = True
            while deleted:
                possible_set, deleted1 = Pointed(possible_set)
                possible_set, deleted2 = naked_pair(possible_set)
                possible_set, deleted3 = hidden_pair(possible_set)

                if deleted1 or deleted2 or deleted3:
                    deleted = True
                else:
                    deleted = False


            found, row, column, digit, message = LastPossibleSpot(solving_grid, possible_set)
            if found:
                which_row_col_box = 'Last Spot ' + message
                return found, row, column, digit,which_row_col_box
            else:
                found, row, column, digit = LastDigit(solving_grid, possible_set)
                if found:
                    return found, row, column, digit, 'Last Digit'
                else:
                    return found, None, None, None, 'No Easy Solution'




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
    solution_intuitive = EasySolvePointedAndPair(complete_grid_swapped)
    if solution_intuitive == complete_grid:

        return complete_grid_swapped, complete_grid
    else:

        return GenerateSudoku(number_of_digits)

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
    rand_int = random.randint(1, 14)
    rand_amount_digits = 24 + rand_int

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


    example_set = [[set() for i in range(9)] for j in range(9)]
    '''
    #SET 1 TO TEST HIDDENPAIR/NAKEDPAIR/POINTED
    example_set[0] = [{}, {}, {}, {}, {}, {}, {}, {}, {}]
    example_set[1] = [{3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}]
    example_set[2] = [{4,6}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}, {3,4,5,6,7,8,9}]
    example_set[3] = [{4,6}, {3, 7}, {3, 9}, {3, 9}, {2, 5}, set(), {2, 5}, set(), {2, 4, 5, 7}]
    example_set[4] = [{3,4,5,6,7,8}, {1,2,3,4,5,6,7,8,9}, {1,2,3,4,5,6,7,8,9}, {}, {}, {}, {}, {}, {}]
    example_set[5] = [{3,4,5,6,7,8}, {1,2,3,4,5,6,7,8,9}, {1,2,3,4,5,6,7,8,9}, {}, {}, {}, {}, {}, {}]
    example_set[6] = [{5,9}, {1,2,3,4,5,6,7,8,9}, {1,2,3,4,5,6,7,8,9}, {}, {}, {}, {}, {}, {}]
    example_set[7] = [{3,4,5,6,7,8}, {1,2,3,4,5,6,7,8,9}, {1,2,3,4,5,6,7,8,9}, {}, {}, {}, {}, {}, {}]
    example_set[8] = [{5,6,7}, {5,9}, {1,2,3,4,5,6,7,8,9}, {}, {}, {}, {}, {}, {}]
    for i in range(9):
        print(example_set[i])
    print('--------------------------------')
    hidden_pair(example_set)
    print('--------------------------------')
    for i in range(9):
        print(example_set[i])

    #SET 2
    example_set[0] = [{2,3,4,5,7,8,9}, {1,2,3,4,5,7,8}, {1,2,3,8,9}, {1,5,8,9}, {},{1,5,8,9}, {1,5,8}, {1,5}, {2,9}]
    example_set[1] = [{5,8,9}, {1,5,8}, {1,8,9}, {1,5,8,9}, {}, {}, {}, {}, {}]
    example_set[2] = [{2,5,8,9}, {1,2,5,8}, {}, {}, {}, {1,5,8,9}, {1,5,8}, {}, {2,9}]
    example_set[3] = [{2,3,5}, {}, {}, {1,2,3}, {2,7}, {1,3,7}, {1,5}, {}, {}]
    example_set[4] = [{2,3,5,8}, {1,2,3,5,8}, {1,2,3,8}, {}, {}, {}, {}, {1,5}, {}]
    example_set[5] = [{}, {1,8}, {}, {1,4,8},{}, {1,4,8},  {}, {}, {}]
    example_set[6] = [{}, {2,3,4,7}, {2,3,9}, {2,3,4,6,9}, {2,7}, {3,4,7,9}, {3,6}, {}, {}]
    example_set[7] = [{3,4,9}, {}, {3,9}, {3,4,5,9}, {}, {3,4,5,9}, {}, {}, {}]
    example_set[8] = [{2,3,7,8}, {2,3,7,8}, {}, {2,3,6}, {}, {3,7}, {3,6}, {}, {}]
    for i in range(9):
        print(example_set[i])
    print('--------------------------------')
    hidden_pair(example_set)
    for i in range(9):
        print(example_set[i])
    
    random.seed(20)
    counter_solved_easy = 0
    counter_solved_pointed = 0
    counter_solved_pointed_pair = 0
    for i in range(300):
        grid, complete_grid = GenerateSudoku(32)

        solved_grid1 = EasySolve(grid)
        solved_grid2 = EasySolvePointed(grid)
        solved_grid3 = EasySolvePointedAndPair(grid)

        if solved_grid1 == complete_grid:

            counter_solved_easy += 1

        if solved_grid2 == complete_grid:
            counter_solved_pointed += 1
        if solved_grid3 == complete_grid:
            counter_solved_pointed_pair += 1
        print('ITERATION', i)
    print('-------------------------')
    print('EASY SOLVE', counter_solved_easy)
    print('POINTED SOLVE', counter_solved_pointed)
    print('POINTED AND PAIR SOLVE', counter_solved_pointed_pair)
    '''


