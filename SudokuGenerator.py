import random
from SudokuOpt import sudoku_test, sudoku_test_unique
from pyomo.environ import *


'''
FOR THE GENERATOR WE NEED

- START A GRID WITH A RANDOM NUMBER / ROW           #CHECK
- SOLVE WITH MATH MODEL TO FIND FILLED GRID         #CHECK
- TAKE AWAY NUMBERS, CHECK IF STILL ONLY SOLUTION   #SHOULD WORK
    (-> OBJECTIVE FUNKTION is abs(FILLED GRID - x), if solutions != 0 it is not unique!
- LOOP UNTIL ENOUGH NUMBERS ARE GONE                #SHOULD WORK
- ADD A FUNCTION FOR EVERYTHING TOGETHER
'''

# PROBLEM WITH SKIPPING A NUMBER -> SOLVER ALWAYS USES NONE FOR THAT NUMBER IN OBJECTIVE FUNCTION
# QUICK WORKAROUND, ASK FOR A SOLUTION BIGGER THAN THE NUMBER?!
# PROBLEM SOLVED MAYBE IDK WHO KNOWS AT THIS POINT
def random_grid():


    rand_row = random.randint(1, 9)
    rand_col = random.randint(1, 9)
    rand_digit = random.randint(1, 9)

    random_grid = [[0 for i in range(9)] for j in range(9)]
    random_grid[rand_row - 1][rand_col - 1] = rand_digit

    filled_grid = sudoku_test(random_grid, False)
    return filled_grid

def random_grid2():


    SOMETHING_WENT_WRONG = False
    random_first_row = [i+1 for i in range(9)]
    random.shuffle(random_first_row)
    random_grid = [[0 for i in range(9)] for j in range(9)]
    random_grid[0] = random_first_row
    random_filled_grid = sudoku_test(random_grid, False)

    return random_filled_grid

def take_away_number(grid, filled_grid):
    '''
    FILLED GRID WIRD GERADE AUCH AUSEINANDER GENOMMEN
    UNIQUE TEST KLAPPT NICHT?
    '''
    grid_without_number = grid[:]
    got_rid_of_number = False
    counter = 0

    while got_rid_of_number == False and counter < 81:

        rand_row = random.randint(0,8)
        rand_col = random.randint(0,8)

        if grid[rand_row][rand_col] != 0:
            number = grid[rand_row][rand_col]

            grid_without_number[rand_row][rand_col] = 0
            solution = sudoku_test_unique(grid_without_number, filled_grid, False)
            if solution==0:
                got_rid_of_number = True
            else:
                grid_without_number[rand_row][rand_col] = number
        counter += 1


    return grid_without_number, counter

def get_random_sudoku(number_of_digits):
    # Go through randomized list of the 81 digits,

    temp = list(range(81))
    random.shuffle(temp)

    grid = random_grid2()
    complete_grid = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            complete_grid[i][j] = grid[i][j]


    counter = 0
    for i in range(81):
        random_row = temp[i] // 9
        random_column = temp[i] % 9

        if grid[random_row][random_column] != 0:
            number = grid[random_row][random_column]

            grid[random_row][random_column] = 0
            solution = sudoku_test_unique(grid, complete_grid, False)
            if abs(solution)>0:
                grid[random_row][random_column] = number
            else:
                counter += 1
                if counter == (81 - number_of_digits):
                    break
    return grid, complete_grid

def present_sudoku(grid):
    for i in range(9):
        temp_list = [[] for i in range(3)]
        for j in range(3):
            for k in range(3):
                temp_list[j].append(grid[i][3*j+k])
        print(temp_list[0], '  ', temp_list[1], '  ', temp_list[2])
        if i % 3 == 2:
            print()
    return

if __name__ == '__main__':


    random.seed(12)
    number_of_given_digits = 60

    grid_test  = random_grid2()
    complete_grid = grid_test.copy()

    sudoku1, sudoku1solution = get_random_sudoku(number_of_given_digits)
    present_sudoku(sudoku1solution)
    '''
    # NEED THIS TO CREATE A DIFFERENT LIST, DONT ASK PLEASE
    complete_grid_test = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            complete_grid_test[i][j] = grid_test[i][j]


    counter_digits = 0
    for i in range(81-number_of_given_digits):
        grid_minus_one, counter = take_away_number(grid_test, complete_grid_test)
        if counter < 81:
            counter_digits += 1
        else:
            print('DIDNT WORK')
    print(81-counter_digits)
    print(grid_minus_one)
    print(complete_grid_test)
    '''



    #random_grid2 = random_grid2(7)
    #print(random_grid2)
