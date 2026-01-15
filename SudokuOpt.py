#from pyomo.core import ConcreteModel
#from pyscipopt import Model
from pyomo.environ import *
import os
import sys
import logging

logging.getLogger('pyomo.core').setLevel(logging.ERROR)

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
    opt = solver.solve(model, tee=tee_test)
    return opt

def transfrom_solution_back(model, tee_solution):
    new_grid = [[0 for i in range(9)] for j in range(9)]
    for row in range(9):
        for col in range(9):
            for number in range(9):
                if model.x[row,col,number].value == 1:
                    new_grid[row][col] = number+1
    if tee_solution:
        '''
        print('SOLUTION IS: ')
        for i in range(9):
            print(new_grid[i])
        '''
    return new_grid

def transform_grid_to_binary(grid):
    new_grid = [[[0 for d in range(9)] for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            for d in range(9):
                if grid[i][j] == d+1:
                    new_grid[i][j][d] = 1
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
        '''
        summe = 0
        for i in range(9):
            for j in range(9):
                summand1 = solution_grid[i][j]
                summand2 = 0
                for d in range(9):
                    if model.x[i,j,d].value != None:
                        summand2 += model.x[i,j,d].value*(d+1)
                summe += abs(summand2 - summand1)
        return summe
        '''
        return 0

        #return (sum(abs(model.x[i, j, k]*(k+1) - solution_grid[i][j]) for i in model.row for j in model.column for k in model.digit))

    '''
    Objective function to check if there is another solution but the given solution_grid

    '''

    model.obj = Objective(rule=objective_rule_unique, sense=maximize)

    solver = SolverFactory('scip',
                           executable='D:\\scipoptsuite-10.0.0-win-x64_ZIP\\scipoptsuite-10.0.0-win-x64\\bin\\scip')
    solver.options['limits/bestsol'] = 2
    opt = solver.solve(model, tee=tee_test)


    if (opt.solver.status == SolverStatus.ok) and (
            opt.solver.termination_condition == TerminationCondition.optimal):
        termination = True
    elif (opt.solver.termination_condition == TerminationCondition.infeasible):
        termination = False
    summe = 0
    for i in range(9):
        for j in range(9):
            summand1 = solution_grid[i][j]
            summand2 = 0
            for d in range(9):
                if model.x[i, j, d].value != None:
                    summand2 += model.x[i, j, d].value * (d + 1)
            summe += abs(summand2 - summand1)

    return summe, termination

def sudoku_test_unique(grid, solution_grid, tee_test):
    '''
    Solve a given Sudoku grid with new objective function:
    Given a specific solution, obj function is max(abs(x-solution))
    If maximum is not 0 the puzzles solution is not unique
    '''
    def constraint_unique(model):
        return sum((1-model.x[i, j, k] if solution_grid_binary[i][j][k]==1 else model.x[i,j,k] for i in range(9) for j in range(9) for k in range(9))) >= 1



    solution_grid_binary = transform_grid_to_binary(solution_grid)
    model = start_model()
    model_new = define_constraints(model)
    model.unique_constraint = Constraint(rule=constraint_unique)

    set_sudoku_parameters(model_new, grid)

    solution_value, termination = solve_model_unique(model_new, solution_grid, tee_test)
    test = transfrom_solution_back(model_new, tee_test)

    return solution_value, termination

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

    problematic_grid = [
        [7,0,0,0,0,0,0,5,0],
        [3,8,0,7,0,2,0,9,1],
        [4,0,0,9,5,0,0,0,0],
        [0,0,0,0,0,0,5,0,3],
        [0,5,4,0,2,0,0,0,6],
        [9,0,0,0,0,0,0,8,0],
        [6,0,0,0,0,7,2,0,9],
        [0,3,7,0,1,0,0,0,0],
        [5,0,1,0,0,6,0,4,0]

    ]
    problematic_grid_solution = [
        [7,1,9,3,4,8,6,5,2],
        [3,8,5,7,6,2,4,9,1],
        [4,6,2,9,5,1,7,3,8],
        [1,7,6,8,9,4,5,2,3],
        [8,5,4,1,2,3,9,7,6],
        [9,2,3,6,7,5,1,8,4],
        [6,4,8,5,3,7,2,1,9],
        [2,3,7,4,1,9,8,6,5],
        [5,9,1,2,8,6,3,4,7]
    ]
    solution_problematic = sudoku_test(problematic_grid, False)

    solution_grid_problematic = [[0 for j in range(9)] for i in range(9)]
    for i in range(9):
        for j in range(9):
            solution_grid_problematic[i][j] = solution_problematic[i][j]

    problematic_value = sudoku_test_unique(problematic_grid, solution_problematic, True)
    binary_problematic = transform_grid_to_binary(problematic_grid_solution)


    '''
    model = start_model()

    model_new = define_constraints(model)

    set_sudoku_parameters(model_new, filled_grid)

    opt_test = solve_model(model_new, tee_test=True)
    solution = transfrom_solution_back(model_new, True)

    empty_grid = [[0 for i in range(9)] for j in range(9)]

    solution_unique = sudoku_test_unique(empty_grid, solution, True)
    '''

