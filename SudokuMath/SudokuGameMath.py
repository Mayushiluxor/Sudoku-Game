import sys

if not sys.stdout:
    class Dummy:
        def write(self, msg): pass
        def flush(self): pass

    sys.stdout = Dummy()
    sys.stderr = Dummy()

import pygame
import pygame_widgets as pw
from pyomo.environ import *
import sys
import time
from pygame_widgets.button import Button
from SudokuSolverMath import sudoku_test
from SudokuGeneratorMath import get_random_sudoku
import multiprocessing
import logging

logging.getLogger('pyomo.core').setLevel(logging.ERROR)

'''
SUDOKU GAME FROM "The-Assembly"
https://github.com/The-Assembly/Code-an-AI-Sudoku-Solver-in-Python

TODO 
    Code a generator of sudoku puzzles
x   Solve with math optimization
    Create button/key to revert last digit
    Let it overwrite numbers after input
'''


def DrawGrid():
    global grid, complete_grid, counter
    # Draw the lines
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # filling the non-empty cells
                pygame.draw.rect(screen, (255,204,204), (i * inc, j * inc, inc + 1, inc + 1))
                # inserting the default values
                text = a_font.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(text, (i * inc + 18, j * inc + 10))
            elif len(guesses[i][j]) > 0:
                pass
            else:
                pygame.draw.rect(screen, (255,229,204), (i * inc, j * inc, inc + 1, inc + 1))
    # Draw lines horizontally and vertically to form grid
    for i in range(10):
        if i % 3 == 0:
            width = 6  # every 3 small boxes -> thicker line
        else:
            width = 3
        pygame.draw.line(screen, (0, 0, 0), (i * inc, 0), (i * inc, width_screen-4), width)  # vertical
        pygame.draw.line(screen, (0, 0, 0), (0, i * inc), (width_screen-4, i * inc), width)  # horizontal


# Solving with mathematical mixed integer model
def Solve_Mathematical(gridArray):
    global complete_grid, counter
    grid = sudoku_test(gridArray, False)
    for i in range(9):
        for j in range(9):
            gridArray[i][j] = grid[i][j]


# setting the initial position
def SetMousePosition(p):
    global x, y, complete_grid, counter
    if p[0] < width_screen and p[1] < width_screen:
        x = p[0] // inc
        y = p[1] // inc


def IsUserValueValid(grid, complete_grid, row,col, value):
    if round(complete_grid[row][col]) == round(value):

        return True
    else:
        return False


# highlighting the selected cell
def DrawSelectedBox():
    global grid, complete_grid, counter
    if int(x) > 8 or int(y) > 8 or int(x) < 0 or int(y) < 0:
        return

    for i in range(2):
        pygame.draw.line(screen, (0, 0, 255), (x * inc, (y + i) * inc), (x * inc + inc, (y + i) * inc), 5)
        pygame.draw.line(screen, (0, 0, 255), ((x + i) * inc, y * inc), ((x + i) * inc, y * inc + inc), 5)

    Value = grid[int(x)][int(y)]
    for i in range(9):
        for j in range(9):
            if grid[i][j] == Value:
                if grid[i][j] != 0:
                    text = a_font.render(str(grid[i][j]), True, (0, 0, 200))
                    screen.blit(text, (i * inc + 18, j * inc + 10))


# insert value entered by user
def InsertValue(Value):
    global grid, complete_grid, counter
    grid[int(x)][int(y)] = Value
    guesses[x][y].clear()
    text = a_font.render(str(Value), True, (0, 0, 0))
    screen.blit(text, (x * inc + 15, y * inc + 15))



def InsertGuess(value, x, y):
    global grid, complete_grid, counter
    if value in guesses[x][y]:
        guesses[x][y].remove(value)   # toggle off
    else:
        guesses[x][y].add(value)      # toggle on

def DrawGuesses():
    global GuessValue, grid, complete_grid, counter
    if GuessValue > 0:
        if grid[int(x)][int(y)] == 0:
            InsertGuess(GuessValue, x, y)
            pygame.draw.rect(screen, (255, 229, 204), (x * inc, y * inc, inc + 1, inc + 1))
            for value in guesses[x][y]:
                #text = guess_font.render(str(GuessValue), True, (120, 120, 120))
                text = b_font.render(str(value), True, (0, 0, 0))

                # position inside the cell (3x3 grid)
                row = (value - 1) // 3
                col = (value - 1) % 3

                pos_x = x * inc + 5 + col * (inc // 3)
                pos_y = y * inc + 5 + row * (inc // 3)
                screen.blit(text, (pos_x, pos_y))
                GuessValue = 0
        GuessValue = 0

def IsUserWin():
    global grid, complete_grid, counter
    for i in range(9):
        for j in range(9):
            if grid[int(i)][int(j)] == 0:
                return False
    return True

def DrawCounter():
    global grid, complete_grid, counter
    TitleFont = pygame.font.SysFont("times", 30, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)
    for i in range(9):
        pygame.draw.rect(screen, (255, 255, 255), rect=(i * inc + 8, 510, 40, 40))
        pygame.draw.rect(screen, (255, 255, 255), (i * inc + 8, 550, 40, 40))
        if counter[i] != 9:
            text_digit = TitleFont.render(str(i + 1), True, (0, 0, 0))
            text_counter = AttributeFont.render(str(counter[i]), True, (0, 0, 0))
        else:
            text_digit = TitleFont.render(str(i + 1), True, (160,160,160))
            text_counter = AttributeFont.render(str(counter[i]), True, (160,160,160))

        screen.blit(text_digit, (i*inc + 18,510))
        screen.blit(text_counter, (i * inc + 22, 550))


def DrawModes():
    global grid, complete_grid, counter
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)
    screen.blit(TitleFont.render("Game Settings", True, (0, 0, 0)), (15, 605))
    screen.blit(AttributeFont.render("C: Clear", True, (0, 0, 0)), (30, 630))
    screen.blit(TitleFont.render("Modes", True, (0, 0, 0)), (15, 655))
    screen.blit(AttributeFont.render("E: Easy", True, (0, 0, 0)), (30, 680))
    screen.blit(AttributeFont.render("A: Average", True, (0, 0, 0)), (30, 705))
    screen.blit(AttributeFont.render("H: Hard", True, (0, 0, 0)), (30, 730))






def DrawSolveButton():
    global grid, complete_grid, counter
    events = pygame.event.get()
    Button = pw.button.Button(
        screen, 350, 700, 120, 50, text='Solve',
        fontSize=20, margin=20,
        inactiveColour=(0, 0, 255),
        hoverColour=(0,0,0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: Solve_Mathematical(grid))

    Button.draw()
    pw.update(events)


def DisplayMessage(Message, Interval, Color):
    global grid, complete_grid, counter
    screen.blit(a_font.render(Message, True, Color), (220, 630))
    pygame.display.update()
    pygame.time.delay(Interval)
    screen.fill((255, 255, 255))
    DrawModes()
    DrawSolveButton()


def SetGridMode(Mode):
    global grid, complete_grid, counter
    screen.fill((255, 255, 255))
    DrawModes()
    DrawSolveButton()
    if Mode == 0:  # For clearing the grid
        grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    elif Mode == 1:  # For easy mode
        grid, complete_grid = get_random_sudoku(35)
    elif Mode == 2:  # For average mode
        grid, complete_grid = get_random_sudoku(30)

    elif Mode == 3:  # For hard mode
        grid, complete_grid = get_random_sudoku(25)




def HandleEvents():
    global IsRunning, grid, complete_grid,  x, y, UserValue, GuessValue, counter
    events = pygame.event.get()
    for event in events:
        # Quit the game window
        if event.type == pygame.QUIT:
            IsRunning = False
            sys.exit()
        # Get the mouse position to insert number
        if event.type == pygame.MOUSEBUTTONDOWN:
            SetMousePosition(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if not IsSolving:
                if event.key == pygame.K_LEFT:
                    x -= 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                if event.key == pygame.K_UP:
                    y -= 1
                if event.key == pygame.K_DOWN:
                    y += 1

                #if event.key == pygame.K_1:
                #    UserValue = 1
                if event.key == pygame.K_1:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        GuessValue = 1
                    else:
                        UserValue = 1
                if event.key == pygame.K_2:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        GuessValue = 2
                    else:
                        UserValue = 2
                if event.key == pygame.K_3:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        GuessValue = 3
                    else:
                        UserValue = 3

                if event.key == pygame.K_4:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        GuessValue = 4
                    else:
                        UserValue = 4
                if event.key == pygame.K_5:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        GuessValue = 5
                    else:
                        UserValue = 5
                if event.key == pygame.K_6:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        GuessValue = 6
                    else:
                        UserValue = 6
                if event.key == pygame.K_7:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        GuessValue = 7
                    else:
                        UserValue = 7
                if event.key == pygame.K_8:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        GuessValue = 8
                    else:
                        UserValue = 8
                if event.key == pygame.K_9:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        GuessValue = 9
                    else:
                        UserValue = 9
                if event.key == pygame.K_c:
                    SetGridMode(0)
                if event.key == pygame.K_e:
                    SetGridMode(1)
                if event.key == pygame.K_a:
                    SetGridMode(2)
                if event.key == pygame.K_h:
                    SetGridMode(3)
    Button = pw.button.Button(
        screen, 350, 700, 120, 50, text='Solve',
        fontSize=20, margin=20,
        inactiveColour=(0, 0, 255),
        hoverColour=(255, 255, 255),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: Solve_Mathematical(grid))

    Button.draw()
    pw.update(events)



def DrawUserValue():
    global UserValue, IsSolving, grid, complete_grid, counter
    if UserValue > 0:
        if IsUserValueValid(grid, complete_grid, x, y, UserValue):
            if grid[int(x)][int(y)] == 0:
                InsertValue(UserValue)
                DrawGrid()
                DrawCounter()
                UserValue = 0
                if IsUserWin():
                    IsSolving = False
                    DisplayMessage("YOU WON!!!!", 5000, (0, 255, 0))
            else:
                UserValue = 0
        else:
            if grid[int(x)][int(y)] == 0:
                pygame.draw.rect(screen, (255, 0, 0), (x * inc, y * inc, inc + 1, inc + 1))
                pygame.display.update()
                time.sleep(1)
                pygame.draw.rect(screen, (255, 229, 204), (x * inc, y * inc, inc + 1, inc + 1))
                if len(guesses[x][y]) > 0:
                    InsertGuess(GuessValue, x, y)
                    pygame.draw.rect(screen, (255, 229, 204), (x * inc, y * inc, inc + 1, inc + 1))
                    for value in guesses[x][y]:
                        # text = guess_font.render(str(GuessValue), True, (120, 120, 120))
                        text = b_font.render(str(value), True, (0, 0, 0))

                        # position inside the cell (3x3 grid)
                        row = (value - 1) // 3
                        col = (value - 1) % 3

                        pos_x = x * inc + 5 + col * (inc // 3)
                        pos_y = y * inc + 5 + row * (inc // 3)
                        screen.blit(text, (pos_x, pos_y))



                #DisplayMessage("Incorrect Value", 500, (255, 0, 0))
            for i in range(9):
                text = a_font.render(str(i + 1), True, (0, 0, 0))
                screen.blit(text, (i * inc + 18, 510))
                text = b_font.render(str(counter[i]), True, (0, 0, 0))
                screen.blit(text, (i * inc + 18, 550))
            UserValue = 0

def InitializeComponent():
    global grid, complete_grid, counter
    DrawGrid()
    DrawSelectedBox()
    DrawModes()
    DrawSolveButton()
    pygame.display.update()


def GameThread():
    global grid, complete_grid, counter
    InitializeComponent()
    while IsRunning:
        HandleEvents()
        DrawGrid()
        DrawSelectedBox()
        DrawUserValue()
        DrawGuesses()
        counter = CheckCounter()
        DrawCounter()
        pygame.display.update()

def CheckCounter():
    global grid, complete_grid, counter
    counter = [0 for i in range(9)]
    for i in range(9):
        for j in range(9):
            if grid[i][j] > 0:
                counter[grid[i][j]-1] += 1
    return counter


def main():

    global width_screen, height_screen, screen, a_font, b_font
    global inc, x, y, UserValue, GuessValue, grid, complete_grid, counter
    global IsRunning, IsSolving, guesses, guess_font

    width_screen = 500
    height_screen = 775
    pygame.font.init()
    screen = pygame.display.set_mode((width_screen, height_screen))  # Window size
    screen.fill((255, 255, 255))
    pygame.display.set_caption("SudokuApp")
    a_font = pygame.font.SysFont("times", 30, "bold")  # Different fonts to be used
    b_font = pygame.font.SysFont("times", 15, "bold")
    inc = width_screen // 9  # Screen size // Number of boxes = each increment
    x = 0
    y = 0
    UserValue = 0
    GuessValue = 0
    grid, complete_grid = get_random_sudoku(30)
    IsRunning = True
    IsSolving = False
    guesses = [[set() for _ in range(9)] for _ in range(9)]
    guess_font = pygame.font.SysFont(None, 20)


    GameThread()  #


if __name__ == '__main__':

    multiprocessing.freeze_support()
    main()

    '''
    width_screen = 500
    height_screen = 675
    pygame.font.init()
    screen = pygame.display.set_mode((width_screen, height_screen))  # Window size
    screen.fill((255, 255, 255))
    pygame.display.set_caption("SudokuApp")
    a_font = pygame.font.SysFont("times", 30, "bold")  # Different fonts to be used
    b_font = pygame.font.SysFont("times", 15, "bold")
    inc = width_screen // 9  # Screen size // Number of boxes = each increment
    x = 0
    y = 0
    UserValue = 0
    GuessValue = 0
    grid, complete_grid = get_random_sudoku(30)
    IsRunning = True
    IsSolving = False
    guesses = [[set() for _ in range(9)] for _ in range(9)]
    guess_font = pygame.font.SysFont(None, 20)

    GameThread()
    '''