import pygame
import pygame_widgets as pw
import sys
from pygame_widgets.button import Button
from SudokuOpt import sudoku_test
from SudokuGenerator import get_random_sudoku

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
    '''
    FOR COLOURS:

    CURRENTLY : (204, 102, 153) PINKISH?

    :return:
    '''
    # Draw the lines
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # filling the non-empty cells
                pygame.draw.rect(screen, (255,204,204), (i * inc, j * inc, inc + 1, inc + 1))
                # inserting the default values
                text = a_font.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(text, (i * inc + 18, j * inc + 10))
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
    grid = sudoku_test(gridArray, False)
    for i in range(9):
        for j in range(9):
            gridArray[i][j] = grid[i][j]


# setting the initial position
def SetMousePosition(p):
    global x, y
    if p[0] < width_screen and p[1] < width_screen:
        x = p[0] // inc
        y = p[1] // inc


'''
# checks if inserted val is valid
def IsUserValueValid(m, i, j, v):
    for ii in range(9):
        if m[i][ii] == v or m[ii][j] == v:  # checks cols and rows
            return False
    # checks the box/block
    ii = i // 3
    jj = j // 3
    for i in range(ii * 3, ii * 3 + 3):
        for j in range(jj * 3, jj * 3 + 3):
            if m[i][j] == v:
                return False
    return True
'''
def IsUserValueValid(grid, completed_grid, row,col, value):
    if completed_grid[row][col] == value: return True
    return False


# highlighting the selected cell
def DrawSelectedBox():
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
    grid[int(x)][int(y)] = Value
    guesses[x][y].clear()
    text = a_font.render(str(Value), True, (0, 0, 0))
    screen.blit(text, (x * inc + 15, y * inc + 15))

def InsertGuess(value, x, y):
    if value in guesses[x][y]:
        guesses[x][y].remove(value)   # toggle off
    else:
        guesses[x][y].add(value)      # toggle on

def DrawGuesses():
    global GuessValue
    if GuessValue > 0:
        for value in guesses[x][y]:
            text = guess_font.render(str(value), True, (120, 120, 120))

            # position inside the cell (3x3 grid)
            row = (value - 1) // 3
            col = (value - 1) % 3

            pos_x = x * inc + 5 + col * (inc // 3)
            pos_y = y * inc + 5 + row * (inc // 3)

            screen.blit(text, (pos_x, pos_y))
            GuessValue = 0

def IsUserWin():
    for i in range(9):
        for j in range(9):
            if grid[int(i)][int(j)] == 0:
                return False
    return True


def DrawModes():
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)
    screen.blit(TitleFont.render("Game Settings", True, (0, 0, 0)), (15, 505))
    screen.blit(AttributeFont.render("C: Clear", True, (0, 0, 0)), (30, 530))
    screen.blit(TitleFont.render("Modes", True, (0, 0, 0)), (15, 555))
    screen.blit(AttributeFont.render("E: Easy", True, (0, 0, 0)), (30, 580))
    screen.blit(AttributeFont.render("A: Average", True, (0, 0, 0)), (30, 605))
    screen.blit(AttributeFont.render("H: Hard", True, (0, 0, 0)), (30, 630))


def DrawSolveButton():
    events = pygame.event.get()
    Button = pw.button.Button(
        screen, 350, 600, 120, 50, text='Solve',
        fontSize=20, margin=20,
        inactiveColour=(0, 0, 255),
        hoverColour=(0,0,0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: Solve_Mathematical(grid))

    Button.draw()
    pw.update(events)


def DisplayMessage(Message, Interval, Color):
    screen.blit(a_font.render(Message, True, Color), (220, 530))
    pygame.display.update()
    pygame.time.delay(Interval)
    screen.fill((255, 255, 255))
    DrawModes()
    DrawSolveButton()


def SetGridMode(Mode):
    global grid
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
        grid, completed_grid = get_random_sudoku(35)
    elif Mode == 2:  # For average mode
        grid, completed_grid = get_random_sudoku(30)
    elif Mode == 3:  # For hard mode
        grid, completed_grid = get_random_sudoku(25)



def HandleEvents():
    global IsRunning, grid, x, y, UserValue, GuessValue
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
                    if event.key == pygame.K_LSHIFT:
                        print('SHIFT')
                        GuessValue = 1
                    else:
                        UserValue = 1
                if event.key == pygame.K_2:
                    UserValue = 2
                if event.key == pygame.K_3:
                    UserValue = 3
                if event.key == pygame.K_4:
                    UserValue = 4
                if event.key == pygame.K_5:
                    UserValue = 5
                if event.key == pygame.K_6:
                    UserValue = 6
                if event.key == pygame.K_7:
                    UserValue = 7
                if event.key == pygame.K_8:
                    UserValue = 8
                if event.key == pygame.K_9:
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
        screen, 350, 600, 120, 50, text='Solve',
        fontSize=20, margin=20,
        inactiveColour=(0, 0, 255),
        hoverColour=(255, 255, 255),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: Solve_Mathematical(grid))

    Button.draw()
    pw.update(events)



def DrawUserValue():
    global UserValue, IsSolving
    if UserValue > 0:
        if IsUserValueValid(grid, complete_grid, x, y, UserValue):
            if grid[int(x)][int(y)] == 0:
                InsertValue(UserValue)
                UserValue = 0
                if IsUserWin():
                    IsSolving = False
                    DisplayMessage("YOU WON!!!!", 5000, (0, 255, 0))
            else:
                UserValue = 0
        else:
            DisplayMessage("Incorrect Value", 500, (255, 0, 0))
            UserValue = 0

def InitializeComponent():
    DrawGrid()
    DrawSelectedBox()
    DrawModes()
    DrawSolveButton()
    pygame.display.update()


def GameThread():
    InitializeComponent()
    while IsRunning:
        HandleEvents()
        DrawGrid()
        DrawSelectedBox()
        DrawUserValue()
        DrawGuesses()
        pygame.display.update()


if __name__ == '__main__':
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
    print(guesses)

    GameThread()