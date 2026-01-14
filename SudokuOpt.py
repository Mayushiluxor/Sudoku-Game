#from pyomo.core import ConcreteModel
#from pyscipopt import Model
from pyomo.environ import *
import os
import sys

'''
SOLVING SUDOKU and creating sudoku grid out of nothing
Variables x_row,column,digit
9 rows, 9 columns, 9 digits
9^3 -> 729 Variables
'''

'''
Sudoku rules: Only 1 digit per row, column and box (3x3 boxes) and 9 variables per slot gives 4 different constraints
'''

'''
for solving sudoku the objective function is irrelevant and we will set it to 0.
The puzzle will only have one solution.

for creating grids we will find a way to work around randomness,
e.g. give a first digit somewhere random on the grid and then let the solver do its work. 
The solution to this puzzle will not be unique, but we dont care about that.

'''

def get_scip_executable():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'solver', 'scip.exe')

def start_model():
    index_for_variables = [(i, j, k) for i in range(9) for j in range(9) for k in range(9)]

    model = ConcreteModel('Test')
    model.row = Set(initialize=range(9))
    model.column = Set(initialize=range(9))
    model.digit = Set(initialize=range(9))
    model.box = Set(initialize=range(9))

    model.x = Var(index_for_variables, domain=Binary)
    return model


def define_constraints(model):
    '''
    Constraints
    every digit only once per row (one_digit_per_row)
    every digit only once per column (one_digit_per_column)
    every digit only once per slot (one_digit_per_slot)
    every digit only once per box (one_digit_per_box)
    '''
    def one_digit_per_row(model, j, k):
        return sum(model.x[i,j,k] for i in model.row) == 1

    model.rows_constraint = Constraint(model.column, model.digit, rule=one_digit_per_row)

    def one_digit_per_column(model, i, k):
        return sum(model.x[i,j,k] for j in model.column) == 1

    model.column_constraint = Constraint(model.row, model.digit, rule=one_digit_per_column)

    def one_digit_per_slot(model, i,j):
        return sum(model.x[i,j,k] for k in model.digit) == 1

    model.slot_constraint = Constraint(model.row, model.column, rule=one_digit_per_slot)



    def one_digit_per_box(model, b, k):
        box_row = b // 3
        box_col = b % 3
        return sum(model.x[i, j, k] for i in range(3 * box_row, 3 * box_row + 3) for j in range(3 * box_col, 3 * box_col + 3)) == 1


    model.box_constraint = Constraint(model.box, model.digit, rule=one_digit_per_box)
    return model

def set_sudoku_parameters(model, grid):
    #new_grid = transform_to_nine_variables(grid)
    number_rows = len(grid)
    number_columns = len(grid[0])
    for row in range(number_rows):
        for col in range(number_columns):
            number = grid[row][col]
            if grid[row][col] > 0:
                model.x[row, col,(number - 1)].fix(1)

def solve_model(model, tee_test):
    '''
   Objective function
   Irrelevant since we only have a unique solution for a normal sudoku.
   For filling the grid we just take any solution
   '''

    def objective_rule(model):
        #return 0

        return (sum(model.x[i, j, k] for i in model.row for j in model.column for k in model.digit))

    '''
    Objective function to check how many digits are being used, should always be 81
    
    '''

    model.obj = Objective(rule=objective_rule, sense=minimize)

    #solver = SolverFactory('scip', executable='D:\\scipoptsuite-10.0.0-win-x64_ZIP\\scipoptsuite-10.0.0-win-x64\\bin\\scip')
    scip_path = get_scip_executable()
    solver = SolverFactory('scip', executable=scip_path)
    opt = solver.solve(model, tee=tee_test, logfile="TEST.txt")
    return opt

def transfrom_solution_back(model, tee_solution):
    new_grid = [[0 for i in range(9)] for j in range(9)]
    for row in range(9):
        for col in range(9):
            for number in range(9):
                if round(model.x[row,col,number].value) == 1:
                    new_grid[row][col] = number+1
    if tee_solution:
        '''
        print('SOLUTION IS: ')
        for i in range(9):
            print(new_grid[i])
        '''
    return new_grid

def sudoku_test(grid, tee_test):
    model = start_model()
    model_new = define_constraints(model)
    set_sudoku_parameters(model_new, grid)
    opt_test = solve_model(model_new, tee_test)
    solution = transfrom_solution_back(model_new, tee_test)

    return solution


def solve_model_unique(model, solution_grid, tee_test):



    def objective_rule_unique(model):
        summe = 0
        for i in range(9):
            for j in range(9):
                summand1 = solution_grid[i][j]
                summand2 = 0
                for d in range(9):
                    if model.x[i,j,d].value != None:
                        summand2 += model.x[i,j,d].value*(d+1)
                summe += abs(summand2 - summand1)
                '''
                if abs(summand1 - summand2) >0:
                    print('SHOW ME')
                    print(summand1, summand2)
                    print(model.x[i,j,6].value)
                    print(i,j)
        print('SUMME' , summe)
        '''
        return summe

        #return (sum(abs(model.x[i, j, k]*(k+1) - solution_grid[i][j]) for i in model.row for j in model.column for k in model.digit))

    '''
    Objective function to check if there is another solution but the given solution_grid

    '''

    model.obj = Objective(rule=objective_rule_unique, sense=maximize)

    solver = SolverFactory('scip',
                           executable='D:\\scipoptsuite-10.0.0-win-x64_ZIP\\scipoptsuite-10.0.0-win-x64\\bin\\scip')
    solver.options['limits/bestsol'] = 1
    opt = solver.solve(model, tee=tee_test, logfile="TEST.txt")

    '''
    for i in range(9):
        for j in range(9):
            print(solution_grid[i][j])
            for d in range(9):
                if round(model.x[i,j,d].value) != 0:
                    print(model.x[i,j,d].value*(d+1))
    '''


    summe = sum(abs(model.x[i, j, k].value)*(k+1) - solution_grid[i][j] for i in model.row for j in model.column for k in model.digit)

    summe = 0
    for i in range(9):
        for j in range(9):
            summand1 = solution_grid[i][j]
            summand2 = 0
            for d in range(9):
                if model.x[i, j, d].value != None:
                    summand2 += model.x[i, j, d].value * (d + 1)
            summe += abs(summand2 - summand1)
    #print('----------------------')
    #print('SUMME:', summe)
    #print('----------------------')
    return summe

def sudoku_test_unique(grid, solution_grid, tee_test):
    '''
    Solve a given Sudoku grid with new objective function:
    Given a specific solution, obj function is max(abs(x-solution))
    If maximum is not 0 the puzzles solution is not unique
    '''



    model = start_model()
    model_new = define_constraints(model)

    set_sudoku_parameters(model_new, grid)

    solution_value = solve_model_unique(model_new, solution_grid, tee_test)
    test = transfrom_solution_back(model_new, tee_test)
    return solution_value

if __name__ == '__main__':
    filled_grid = [[0, 5, 0, 9, 0, 0, 1, 6, 0],
                   [9, 0, 0, 0, 0, 0, 8, 0, 0],
                   [0, 0, 4, 0, 0, 0, 0, 0, 5],
                   [7, 0, 3, 4, 0, 0, 0, 5, 1],
                   [0, 2, 0, 0, 5, 7, 0, 0, 0],
                   [5, 0, 0, 0, 0, 0, 7, 0, 0],
                   [8, 0, 0, 0, 4, 0, 0, 3, 0],
                   [2, 0, 0, 3, 0, 0, 0, 1, 8],
                   [0, 0, 0, 1, 8, 0, 5, 0, 2]]

    model = start_model()

    model_new = define_constraints(model)

    set_sudoku_parameters(model_new, filled_grid)

    opt_test = solve_model(model_new, tee_test=True)
    solution = transfrom_solution_back(model_new, True)

    empty_grid = [[0 for i in range(9)] for j in range(9)]

    solution_unique = sudoku_test_unique(empty_grid, solution, True)

