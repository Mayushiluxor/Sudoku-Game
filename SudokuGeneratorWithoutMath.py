import pygame

from SudokuSolverWIthoutMath import *
import random

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
    complete_grid = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            complete_grid[i][j] = grid[i][j]
    complete_grid_swapped = SwapDigitsRandom(grid)

    counter = 0

    for i in range(81):
        random_row = temp[i] // 9
        random_column = temp[i] % 9


        if grid[random_row][random_column] != 0:
            number = grid[random_row][random_column]

            grid[random_row][random_column] = 0
            solution, counter_solutions = SudokuGrid(grid)


            if counter_solutions >1:
                grid[random_row][random_column] = number
            elif counter_solutions == 1:
                counter += 1
                if counter == (81 - number_of_digits):
                    break
    return grid, complete_grid

def SwapDigitsRandom(grid):
    temp = list(range(9))
    random.shuffle(temp)
    print(temp)
    swappedGrid = [[0 for i in range(9)] for j in range(9)]

    for i in range(9):
        for j in range(9):
            old_digit = grid[i][j]
            new_digit = temp[old_digit-1]
            swappedGrid[i][j] = new_digit+1
    return swappedGrid




if __name__ == '__main__':
    random.seed(2)
    number_given_digits = 50

    grid, complete_grid = GenerateSudoku(number_given_digits)

    swappedGrid = SwapDigitsRandom(complete_grid)
    print(swappedGrid)
    print(complete_grid)

