import sys

if not sys.stdout:
    class Dummy:
        def write(self, msg): pass
        def flush(self): pass

    sys.stdout = Dummy()
    sys.stderr = Dummy()

import pygame
import pygame_widgets as pw
import sys
import time
from pygame_widgets.button import Button
from SudokuSolverWIthoutMath import *
#from SudokuGeneratorWithoutMath import *

'''
ORIGINAL CODE FROM https://github.com/The-Assembly/Code-an-AI-Sudoku-Solver-in-Python
MOST THINGS DID NOT WORK, BUT GAME STRUCTURE IS FROM THERE

DONE
HIGHLIGHT NUMBERS WHEN CLICKING ON COUNTING NUMBERS
BLOCK AROUND HIGHLIGHT NUMBER AT COUNTING NUMBERS
CLEAN UP "SETTINGS" NAMES
SOLVE BUTTON COLOR FIX

CLEAN UP "MODES" GETTING CUT OFF
TIMER/FEHLER ON/OFF MODUS
BATU VORSCHLAG 
    - Fehlerbegrenzung 
PAUSE BUTTON/KEYBIND
CLEAN UP "SETTINGS" POSITION MAYBE?
SETMOUSEPOSITION CLEAN UP NUMBER

STOP TIMER WHEN DONE
SHOW TIMER UNTIL NEW GAME IS STARTED

FIXED BUG ON FAULT

HINT / GET SINGLE NUMBER INSTEAD OF SOLVE BUTTON

ONLY GIVE GRIDS THAT ARE SOLVABLE FROM HINTS?

IN A WAY PROBLEM WITH SOLVER -> WHILE CHANGE MEANS EVEN IF HE WOULD FIND SOLUTIONS, HE FIRST ELIMINATES AND WITH THAT ELIMINATES
FIXED THAT 
TODO:

Fixed crash on try insert number on counter number position

HIGHLIGHT HINT CHANGE MAYBE?




'''




def DrawGrid():
    global grid, complete_grid, counter, original_grid
    # Draw the lines
    for i in range(9):
        for j in range(9):
            if original_grid[i][j] != 0:
                # filling the non-empty cells
                pygame.draw.rect(screen, (255, 204, 204), (i * inc, j * inc, inc + 1, inc + 1))
                # inserting the default values
                text = a_font.render(str(grid[i][j]), True, (0,0,0))
                screen.blit(text, (i * inc + 18, j * inc + 10))
            elif grid[i][j] != 0:
                # filling the non-empty cells
                pygame.draw.rect(screen, (255,204,204), (i * inc, j * inc, inc + 1, inc + 1))
                # inserting the default values
                text = c_font.render(str(grid[i][j]), True, (0,0,0))
                screen.blit(text, (i * inc + 18, j * inc + 10))
            elif len(guesses[i][j]) > 0:
                pygame.draw.rect(screen, (255, 229, 204), (i * inc, j * inc, inc + 1, inc + 1))
                for value in guesses[i][j]:
                    text = b_font.render(str(value), True, (0, 0, 0))

                    # position inside the cell (3x3 grid)
                    row = (value - 1) // 3
                    col = (value - 1) % 3

                    pos_x = i * inc + 5 + col * (inc // 3)
                    pos_y = j * inc + 3 + row * (inc // 3)
                    screen.blit(text, (pos_x, pos_y))
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





def SetMousePosition(p):
    global x, y, complete_grid, counter, original_grid
    if p[0] < width_screen and p[1] < width_screen + 80:
        x = p[0] // inc
        y = p[1] // inc



def IsUserValueValid(grid, complete_grid, row,col, value):
    if round(complete_grid[row][col]) == round(value):

        return True
    else:
        return False



# highlighting the selected cell
def DrawSelectedBox():
    global grid, complete_grid, counter, original_grid
    if int(x) > 8 or int(y) > 9 or int(x) < 0 or int(y) < 0:
        return
    if int(y) == 9:
        Value = int(x)+1
        for i in range(2):
            pygame.draw.line(screen, (0, 0, 255), (x * inc, (y + i) * inc), (x * inc + inc, (y + i) * inc), 5)
            pygame.draw.line(screen, (0, 0, 255), ((x + i) * inc, y * inc), ((x + i) * inc, y * inc + inc), 5)
    else:
        for i in range(2):
            pygame.draw.line(screen, (0, 0, 255), (x * inc, (y + i) * inc), (x * inc + inc, (y + i) * inc), 5)
            pygame.draw.line(screen, (0, 0, 255), ((x + i) * inc, y * inc), ((x + i) * inc, y * inc + inc), 5)

        Value = grid[int(x)][int(y)]
    for i in range(9):
        for j in range(9):
            if grid[i][j] == Value:
                if grid[i][j] != 0:
                    pygame.draw.rect(screen, (255, 204, 204), (i * inc+5, j * inc+5, inc + 1-10, inc + 1-10))
                    text = a_font.render(str(grid[i][j]), True, (0, 0, 200))
                    screen.blit(text, (i * inc + 18, j * inc + 10))
            if grid[i][j] == 0:
                for note in guesses[i][j]:
                    if note == Value:
                        text = b_font.render(str(note), True, (0, 0, 255))
                    else:
                        text = b_font.render(str(note), True, (0, 0, 0))

                    # position inside the cell (3x3 grid)
                    row = (note - 1) // 3
                    col = (note - 1) % 3

                    pos_x = i * inc + 5 + col * (inc // 3)
                    pos_y = j * inc + 3 + row * (inc // 3)
                    screen.blit(text, (pos_x, pos_y))


# insert value entered by user
def InsertValue(Value):
    global grid, complete_grid, counter, original_grid
    grid[int(x)][int(y)] = Value
    guesses[x][y].clear()
    text = a_font.render(str(Value), True, (0, 0, 0))
    screen.blit(text, (x * inc + 18, y * inc + 10))



def InsertGuess(value, x, y):
    global grid, complete_grid, counter, original_grid
    if value in guesses[x][y]:
        guesses[x][y].remove(value)   # toggle off
    else:
        guesses[x][y].add(value)      # toggle on

def DrawGuesses():
    global GuessValue, grid, complete_grid, counter, original_grid
    if GuessValue > 0:
        if int(x) <= 8 and int(y) <= 8 and int(x) >= 0 and int(y) >= 0:
            if grid[int(x)][int(y)] == 0:
                InsertGuess(GuessValue, x, y)
                pygame.draw.rect(screen, (255, 229, 204), (x * inc, y * inc, inc + 1, inc + 1))
                for value in guesses[x][y]:

                    text = b_font.render(str(value), True, (0, 0, 0))


                    # position inside the cell (3x3 grid)
                    row = (value - 1) // 3
                    col = (value - 1) % 3

                    pos_x = x * inc + 5 + col * (inc // 3)
                    pos_y = y * inc + 3 + row * (inc // 3)
                    screen.blit(text, (pos_x, pos_y))
                    GuessValue = 0
            GuessValue = 0
        else:
            GuessValue = 0

def IsUserWin():
    global grid, complete_grid, counter, original_grid
    for i in range(9):
        for j in range(9):
            if grid[int(i)][int(j)] == 0:
                return False
    return True

def DrawCounter():
    global grid, complete_grid, counter, original_grid
    TitleFont = pygame.font.SysFont("times", 30, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)
    if int(y) == 9:
        Value = int(x)
    else:
        Value = -1
    for i in range(9):
        if i == Value:
            pygame.draw.rect(screen, (255, 255, 255), rect=(i * inc-5, 499, 66, 66))
            pygame.draw.rect(screen, (255, 255, 255), (i * inc-5, 560, 400, 15))

            if counter[i] != 9:
                text_digit = TitleFont.render(str(i + 1), True, (0, 0, 200))
                text_counter = AttributeFont.render(str(counter[i]), True, (0, 0, 0))
            else:
                text_digit = TitleFont.render(str(i + 1), True, (160,160,160))
                text_counter = AttributeFont.render(str(counter[i]), True, (160,160,160))

            screen.blit(text_digit, (i*inc + 18,505))
            screen.blit(text_counter, (i * inc + 22, 555))
        else:
            pygame.draw.rect(screen, (255, 255, 255), rect=(i * inc - 5, 499, 66, 66))
            pygame.draw.rect(screen, (255, 255, 255), (i * inc - 5, 560, 66, 15))

            if counter[i] != 9:
                text_digit = TitleFont.render(str(i + 1), True, (0, 0, 0))
                text_counter = AttributeFont.render(str(counter[i]), True, (0, 0, 0))
            else:
                text_digit = TitleFont.render(str(i + 1), True, (160, 160, 160))
                text_counter = AttributeFont.render(str(counter[i]), True, (160, 160, 160))

            screen.blit(text_digit, (i * inc + 18, 505))
            screen.blit(text_counter, (i * inc + 22, 555))



def DrawModes():
    global grid, complete_grid, counter, original_grid
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)

    screen.blit(AttributeFont.render("D: Daily", True, (0, 0, 0)), (30, 630))
    screen.blit(TitleFont.render("Modes", True, (0, 0, 0)), (15, 605))
    screen.blit(AttributeFont.render("E: Easy", True, (0, 0, 0)), (30, 655))
    screen.blit(AttributeFont.render("A: Average", True, (0, 0, 0)), (30, 680))
    screen.blit(AttributeFont.render("H: Hard", True, (0, 0, 0)), (30, 705))
    screen.blit(TitleFont.render("Settings", True, (0, 0, 0)), (160, 605))
    screen.blit(AttributeFont.render("T: Timer on/off", True, (0, 0, 0)), (175, 630))
    screen.blit(AttributeFont.render("F: Faults on/off", True, (0, 0, 0)), (175, 655))
    screen.blit(AttributeFont.render("Hints used", True, (0, 0, 0)), (175, 680))
    screen.blit(AttributeFont.render("P: Pause", True, (0, 0, 0)), (175, 705))

    screen.blit(AttributeFont.render("S: Hints Solved/Unsolved", True, (0, 0, 0)), (175, 730))

def CheckAndDraw():
    global grid, complete_grid, counter, original_grid, hint_counter, IsHints
    solved, row_sol, col_sol, digit, which = CheckOneSlot(grid)
    if solved:
        hint_counter += 1
        Hints()
        pygame.draw.rect(screen, (0, 255, 0), (row_sol * inc, col_sol * inc, inc + 1, inc + 1))
        if IsHints:
            message = which +' '+ str(digit)
        else:
            message = which
        DisplayMessage(message, 1000, (0, 0, 0))
        DrawGrid()
        DrawCounter()
        Timer()
        pygame.display.update()
        time.sleep(1)
        pygame.draw.rect(screen, (255, 229, 204), (row_sol * inc, col_sol * inc, inc + 1, inc + 1))
        if len(guesses[row_sol][col_sol]) > 0:
            pygame.draw.rect(screen, (255, 229, 204), (row_sol * inc, col_sol * inc, inc + 1, inc + 1))
            for value in guesses[row_sol][col_sol]:
                text = b_font.render(str(value), True, (0, 0, 0))

                # position inside the cell (3x3 grid)
                row = (value - 1) // 3
                col = (value - 1) % 3

                pos_x = row_sol * inc + 5 + col * (inc // 3)
                pos_y = col_sol * inc + 5 + row * (inc // 3)
                screen.blit(text, (pos_x, pos_y))

    else:
        message = "No easy solution"
        DisplayMessage(message, 2000, (0,0,0))





def DrawSolveButton():
    global grid, complete_grid, counter, original_grid
    events = pygame.event.get()
    Button = pw.button.Button(
        screen, 350, 775, 120, 50, text='Hint',
        fontSize=20, margin=20,
        inactiveColour=(255, 204, 204),
        hoverColour=(255,229,204),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: CheckAndDraw())

    Button.draw()
    pw.update(events)


def DisplayMessage(Message, Interval, Color):
    global grid, complete_grid, counter, original_grid
    screen.blit(a_font.render(Message, True, Color), (70, 765))
    pygame.display.update()
    pygame.time.delay(Interval)
    screen.fill((255, 255, 255))
    DrawModes()
    DrawSolveButton()


def SetGridMode(Mode):
    global grid, complete_grid, counter, original_grid, start_time, Fault_Counter, IsSolving
    screen.fill((255, 255, 255))
    DrawModes()
    DrawSolveButton()
    if Mode == 0:
        grid, complete_grid = GenerateDailySudoku()
        original_grid = [[0 for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                original_grid[i][j] = grid[i][j]
    elif Mode == 1:  # For easy mode
        grid, complete_grid = GenerateSudoku(40)
        original_grid = [[0 for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                original_grid[i][j] = grid[i][j]

    elif Mode == 2:  # For average mode
        grid, complete_grid = GenerateSudoku(32)
        original_grid = [[0 for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                original_grid[i][j] = grid[i][j]


    elif Mode == 3:  # For hard mode
        grid, complete_grid = GenerateSudoku(25)
        original_grid = [[0 for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                original_grid[i][j] = grid[i][j]
    start_time = pygame.time.get_ticks()
    Fault_Counter = 0
    IsSolving = False
    pygame.init()

def TimerChange():
    global IsTimer
    if IsTimer == True:
        IsTimer = False

    else:
        IsTimer = True

def HintsChange():
    global IsHints
    if IsHints == True:
        IsHints = False
    else:
        IsHints = True

def FaultChange():
    global IsFault
    if IsFault == True:
        IsFault = False
    else:
        IsFault = True

def PauseChange():
    global IsPause, paused_time, pause_start
    if IsPause:
        IsPause = False
        paused_time += pygame.time.get_ticks() - pause_start
    else:
        IsPause = True
        pause_start = pygame.time.get_ticks()

def Pause():
    '''
    While being paused an empty grid is being drawn on the screen.
    '''
    if IsPause:
        for i in range(9):
            for j in range(9):
                pygame.draw.rect(screen, (255, 229, 204), (i * inc, j * inc, inc + 1, inc + 1))
    for i in range(10):
        if i % 3 == 0:
            width = 6  # every 3 small boxes -> thicker line
        else:
            width = 3
        pygame.draw.line(screen, (0, 0, 0), (i * inc, 0), (i * inc, width_screen-4), width)  # vertical
        pygame.draw.line(screen, (0, 0, 0), (0, i * inc), (width_screen-4, i * inc), width)  # horizontal



def HandleEvents():
    global IsRunning, grid, complete_grid,  x, y, UserValue, GuessValue, counter, original_grid, IsSolving
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
                if event.key == pygame.K_d:
                    SetGridMode(0)
                if event.key == pygame.K_e:
                    SetGridMode(1)
                if event.key == pygame.K_a:
                    SetGridMode(2)
                if event.key == pygame.K_h:
                    SetGridMode(3)
                if event.key == pygame.K_t:
                    TimerChange()
                if event.key == pygame.K_f:
                    FaultChange()
                if event.key == pygame.K_p:
                    PauseChange()
                if event.key == pygame.K_s:
                    HintsChange()
            else:
                if event.key == pygame.K_d:
                    SetGridMode(0)
                if event.key == pygame.K_e:
                    SetGridMode(1)
                if event.key == pygame.K_a:
                    SetGridMode(2)
                if event.key == pygame.K_h:
                    SetGridMode(3)
                IsSolving = False

    Button = pw.button.Button(
        screen, 350, 775, 120, 50, text='Hint',
        fontSize=20, margin=20,
        inactiveColour=(255, 204, 204),
        hoverColour=(255,229,204),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: CheckAndDraw())

    Button.draw()
    pw.update(events)



def DrawUserValue():
    global UserValue, IsSolving, grid, complete_grid, counter, original_grid, IsFault, Fault_Counter, start_time, paused_time, IsPause
    if int(x) <= 8 and int(y) <= 8 and int(x) >= 0 and int(y) >= 0:
        if UserValue > 0:
            if IsUserValueValid(grid, complete_grid, x, y, UserValue):
                if grid[int(x)][int(y)] == 0:
                    InsertValue(UserValue)
                    DrawGrid()
                    DrawCounter()
                    UserValue = 0
                    if IsUserWin():
                        IsSolving = True
                        current_time = pygame.time.get_ticks()
                        elapsed_ms = current_time - start_time - paused_time
                        elapsed_seconds = elapsed_ms // 1000

                        minutes = elapsed_seconds // 60
                        seconds = elapsed_seconds % 60
                        time_string = f"{minutes:02}:{seconds:02}"

                        font = pygame.font.SysFont(None, 30)
                        time_surface = font.render(time_string, True, (0, 0, 0))
                        DisplayMessage("WON", 5000, (0, 255, 0))


                        pygame.draw.rect(screen, (255, 255, 255), (375, 600, 100, 100))
                        screen.blit(time_surface, (375, 630))



                else:
                    UserValue = 0
            else:
                if grid[int(x)][int(y)] == 0:
                    pygame.draw.rect(screen, (255, 0, 0), (x * inc, y * inc, inc + 1, inc + 1))
                    pygame.display.update()
                    time.sleep(1)
                    pygame.draw.rect(screen, (255, 229, 204), (x * inc, y * inc, inc + 1, inc + 1))
                    if len(guesses[x][y]) > 0:
                        pygame.draw.rect(screen, (255, 229, 204), (x * inc, y * inc, inc + 1, inc + 1))
                        for value in guesses[x][y]:
                            text = b_font.render(str(value), True, (0, 0, 0))

                            # position inside the cell (3x3 grid)
                            row = (value - 1) // 3
                            col = (value - 1) % 3

                            pos_x = x * inc + 5 + col * (inc // 3)
                            pos_y = y * inc + 5 + row * (inc // 3)
                            screen.blit(text, (pos_x, pos_y))
                    if IsFault:
                        Fault_Counter +=1
                        if Fault_Counter >= 3:
                            DisplayMessage("LOST", 2000, (255, 0, 0))
                            grid = [[0 for i in range(9)] for j in range(9)]
                            for i in range(9):
                                for j in range(9):
                                    grid[i][j] = original_grid[i][j]
                            start_time = pygame.time.get_ticks()
                            Fault_Counter = 0
                            paused_time = 0
                            pygame.init()



                    #DisplayMessage("Incorrect Value", 500, (255, 0, 0))
                for i in range(9):
                    text = a_font.render(str(i + 1), True, (0, 0, 0))
                    screen.blit(text, (i * inc + 18, 510))
                    text = b_font.render(str(counter[i]), True, (0, 0, 0))
                    screen.blit(text, (i * inc + 18, 550))
                UserValue = 0

def Faults():
    global Fault_Counter, IsFault
    if IsFault:
        fault_string = str(Fault_Counter)+"/3"
        font = pygame.font.SysFont(None, 30)
        time_surface = font.render(fault_string, True, (0, 0, 0))

        pygame.draw.rect(screen, (255,255,255), (375, 655, 70, 25))
        screen.blit(time_surface, (375, 655))

def Hints():
    global hint_counter
    pygame.draw.rect(screen, (255, 255, 255), (375, 680, 70, 25))

    font = pygame.font.SysFont(None, 30)
    hint_text = str(hint_counter)
    hint_surface = font.render(hint_text, True, (0, 0, 0))
    screen.blit(hint_surface, (375, 680))

def Timer():
    global IsTimer
    if not IsSolving:
        if not IsPause:
            if IsTimer:
                current_time = pygame.time.get_ticks()
                elapsed_ms = current_time - start_time - paused_time
                elapsed_seconds = elapsed_ms // 1000

                minutes = elapsed_seconds // 60
                seconds = elapsed_seconds % 60
                time_string = f"{minutes:02}:{seconds:02}"

                font = pygame.font.SysFont(None, 30)
                time_surface = font.render(time_string, True, (0, 0, 0))

                pygame.draw.rect(screen, (255, 255, 255), (375,600,100,100))
                screen.blit(time_surface, (375, 630))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (375, 600, 100, 100))
    else:
        pass
def InitializeComponent():
    global grid, complete_grid, counter, original_grid
    DrawGrid()
    DrawSelectedBox()
    DrawModes()
    DrawSolveButton()
    pygame.display.update()


def GameThread():
    global grid, complete_grid, counter, original_grid, start_time
    InitializeComponent()

    while IsRunning:
        HandleEvents()
        DrawGrid()
        counter = CheckCounter()
        DrawCounter()
        DrawSelectedBox()
        DrawUserValue()
        DrawGuesses()

        Timer()
        Faults()
        Hints()
        Pause()


        pygame.display.update()


def CheckCounter():
    global grid, complete_grid, counter, original_grid
    counter = [0 for i in range(9)]
    for i in range(9):
        for j in range(9):
            if grid[i][j] > 0:
                counter[grid[i][j]-1] += 1
    return counter


def main():

    global width_screen, height_screen, screen, a_font, b_font, c_font, start_time
    global inc, x, y, UserValue, GuessValue, grid, complete_grid, counter, original_grid, hint_counter
    global IsRunning, IsSolving, guesses, IsFault, IsTimer, IsPause, IsHints, paused_time, pause_start, Fault_Counter, end_time

    width_screen = 500
    height_screen = 850
    pygame.font.init()
    screen = pygame.display.set_mode((width_screen, height_screen))  # Window size
    screen.fill((255, 255, 255))
    pygame.display.set_caption("SudokuApp")
    a_font = pygame.font.SysFont("times", 30, "bold")  # Different fonts to be used
    b_font = pygame.font.SysFont("times", 15, "bold")
    c_font = pygame.font.SysFont("times", 30, False)

    inc = width_screen // 9  # Screen size // Number of boxes = each increment
    x = 0
    y = 0
    UserValue = 0
    GuessValue = 0
    grid, complete_grid = GenerateSudoku(30)
    original_grid = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            original_grid[i][j] = grid[i][j]
    IsRunning = True
    IsSolving = False
    guesses = [[set() for _ in range(9)] for _ in range(9)]
    IsFault = False
    IsTimer = True
    IsPause = False
    IsHints = False
    Fault_Counter = 0

    start_time = pygame.time.get_ticks()
    paused_time = 0
    pause_start = 0
    end_time = 0

    hint_counter = 0
    pygame.init()


    GameThread()  #

if __name__ == '__main__':
    main()