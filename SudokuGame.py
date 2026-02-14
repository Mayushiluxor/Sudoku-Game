import sys
import shelve

from pygame import RESIZABLE

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
from SudokuSolver import *
#from SudokuGeneratorWithoutMath import *

'''
ORIGINAL GAME STRUCTURE FROM https://github.com/The-Assembly/Code-an-AI-Sudoku-Solver-in-Python


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

Fixed crash on try insert number on counter number position
FIX PAUSE TIMER GETTING RESET ON NEW GAME?

HIGHLIGHT HINT CHANGE MAYBE?

SAVING MIGHT WORK

BUG? SINCE RANDOM SEED BEING SET ONCE DAILY IS USED

SOLVE TIMER FOR LOADED GAME
TODO:

CONTROLLER 

INGAME MUSIC

Current question : when do we want to save ? 
    -   ever iteration of the gameloop to save the current state in case game crashes
    -   just at the end / button to save to have a controlled load/save


CHECK IF VARIABLE WORKS IN ALL

THINKING ABOUT SWAPPING LAYOUT, MODES / SETTINGS TO RIGHT SIDE

EXTENSION DOESNT ALWAYS WORK
'''




def DrawGrid():
    '''
    If grid cell is not empty, draw the number in it -> different font for original numbers and numbers, that were put in from the user
    If grid cell is empty but note is not empty, draw the note in
    Else just draw an empty cell
    '''
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
        pygame.draw.line(screen, (0, 0, 0), (i * inc, 0), (i * inc, width_sudoku-4), width)  # vertical
        pygame.draw.line(screen, (0, 0, 0), (0, i * inc), (width_sudoku-4, i * inc), width)  # horizontal





def SetMousePosition(p):
    '''
    Can only click on something if
        it is on the grid
        it is a bit below the grid (where the numbers being counted are)
    '''
    global x, y, complete_grid, counter, original_grid
    if p[0] < width_sudoku and p[1] < width_sudoku + 80:
        x = p[0] // inc
        y = p[1] // inc



def IsUserValueValid(grid, complete_grid, row,col, value):
    '''
    quick check if the value the user is trying to input is also in the solution grid
    '''
    if round(complete_grid[row][col]) == round(value):

        return True
    else:
        return False



# highlighting the selected cell
def DrawSelectedBox():
    '''
    Highlight the selected cell and highlight the number in the cell -> also every other cell with that number in it
    (as input number or as note)
    '''
    global grid, complete_grid, counter, original_grid
    if int(x) > 8 or int(y) > 9 or int(x) < 0 or int(y) < 0:
        return
    if int(y) == 9:
        # Couting numbers row
        Value = int(x)+1
        for i in range(2):
            pygame.draw.line(screen, (0, 0, 255), (x * inc, (y + i) * inc), (x * inc + inc, (y + i) * inc), 5)
            pygame.draw.line(screen, (0, 0, 255), ((x + i) * inc, y * inc), ((x + i) * inc, y * inc + inc), 5)
    else:
        # Regular cell
        for i in range(2):
            pygame.draw.line(screen, (0, 0, 255), (x * inc, (y + i) * inc), (x * inc + inc, (y + i) * inc), 5)
            pygame.draw.line(screen, (0, 0, 255), ((x + i) * inc, y * inc), ((x + i) * inc, y * inc + inc), 5)

        Value = grid[int(x)][int(y)]
    # go over all the cells, highlight the same number als "Value"
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
    '''
    Insert the given value into the cell, clear the guesses
    '''
    global grid, complete_grid, counter, original_grid, IsSmartNotes
    grid[int(x)][int(y)] = Value
    guesses[x][y].clear()
    text = a_font.render(str(Value), True, (0, 0, 0))
    screen.blit(text, (x * inc + 18, y * inc + 10))
    '''
    if "smart notes" is on, clear notes in the box/column/row with number "Value"
    '''
    if IsSmartNotes:
        '''
        Check box
        '''
        start_row = x - (x % 3)
        start_col = y - (y % 3)
        for row in range(3):
            for col in range(3):
                if Value in guesses[start_row+row][start_col+col]:
                    guesses[start_row + row][start_col + col].remove(Value)
        '''
        Check row
        '''
        for i in range(9):
            if Value in guesses[x][i]:
                guesses[x][i].remove(Value)
        '''
        Check column
        '''
        for j in range(9):
            if Value in guesses[j][y]:
                guesses[j][y].remove(Value)




def InsertGuess(value, x, y):
    '''
    If number was already in the notes, remove it from the notes, else put it in as a note
    '''
    global grid, complete_grid, counter, original_grid
    if value in guesses[x][y]:
        guesses[x][y].remove(value)   # toggle off
    else:
        guesses[x][y].add(value)      # toggle on

def DrawGuesses():
    '''
    If note is being input (guessvalue > 0) input that as a note, draw all the notes in the box again
    If we are trying to input a note outside of our grid, just ignore it (else part)
    '''
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
    '''
    If whole board is fill, we won!
    '''
    global grid, complete_grid, counter, original_grid
    for i in range(9):
        for j in range(9):
            if grid[int(i)][int(j)] == 0:
                return False
    return True

def DrawCounter():
    '''
    Draw counting numbers
    If we are clicking on that counter, we highlight that number
    Else we have black numbers counting up if we have 0-8 numbers of a specific digit, grey numbers if we have all 9 numbers of a specific digit
    '''
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

def DrawHints():
    '''
    Draw "solved" or "unsolved" depending on hints setting (IsHints)
    '''
    global grid, complete_grid, original_grid, IsHints
    AttributeFont = pygame.font.SysFont("times", 20)
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    font = pygame.font.SysFont(None, 30)

    pygame.draw.rect(screen, (255,255,255), rect = (760, 205, 80, 20))
    if IsHints:
        screen.blit(font.render("Solved", True, (0, 0, 0)), (760, 205))
    else:
        screen.blit(font.render("Unsolved", True, (0, 0, 0)), (760, 205))

def DrawPause():
    '''
    Draw "paused" depending on pause setting (IsPause)
    '''
    global IsPause
    AttributeFont = pygame.font.SysFont("times", 20)
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    font = pygame.font.SysFont(None, 30)
    pygame.draw.rect(screen, (255, 255, 255), rect=(760, 280, 80, 20))
    if IsPause:
        screen.blit(font.render("Paused", True, (0, 0, 0)), (760, 280))


def DrawModes():
    '''
    Draw all the settings
    '''
    global grid, complete_grid, counter, original_grid, IsHints
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)


    screen.blit(TitleFont.render("Modes", True, (0, 0, 0)), (545, 5))
    screen.blit(AttributeFont.render("D: Daily", True, (0, 0, 0)), (560, 30))
    screen.blit(AttributeFont.render("E: Easy", True, (0, 0, 0)), (560, 55))
    screen.blit(AttributeFont.render("A: Average", True, (0, 0, 0)), (560, 80))
    screen.blit(AttributeFont.render("H: Hard", True, (0, 0, 0)), (560, 105))
    screen.blit(TitleFont.render("Settings", True, (0, 0, 0)), (545, 130))
    screen.blit(AttributeFont.render("T: Timer on/off", True, (0, 0, 0)), (560, 155))
    screen.blit(AttributeFont.render("F: Faults on/off", True, (0, 0, 0)), (560, 180))
    #screen.blit(AttributeFont.render("Hints used", True, (0, 0, 0)), (560, 230))
    screen.blit(AttributeFont.render("S: Hint settings", True, (0, 0, 0)), (560, 205))
    screen.blit(AttributeFont.render("P: Pause", True, (0, 0, 0)), (560, 280))
    screen.blit(AttributeFont.render("L: Auto Delete Notes", True, (0, 0, 0)), (560, 230))
    screen.blit(AttributeFont.render("Shift + Number: Note", True, (0, 0, 0)), (560, 305))
    screen.blit(AttributeFont.render("G: Hint", True, (0, 0, 0)), (560, 255))

def CheckAndDraw():
    '''
    Draw a next solution for a single cell in the sudoku grid
    First we get that solution from (CheckOneslot)
    -> if we dont find a solution, message "No easy solution found". How sudokus are being generated, that should never happen
    Highlight the cell and give either the solution strategy or the solution strategy + the solved number
    '''
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
    '''
    Draw the button for the hints

    '''
    global grid, complete_grid, counter, original_grid
    events = pygame.event.get()
    Button = pw.button.Button(
        screen, 750, 530, 120, 50, text='Hint',
        fontSize=20, margin=20,
        inactiveColour=(255, 204, 204),
        hoverColour=(255,229,204),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: CheckAndDraw())

    Button.draw()
    pw.update(events)

def DrawExtendButton():
    '''
    Draw the button for the extension

    '''
    global grid, complete_grid, counter, original_grid
    events = pygame.event.get()
    Button = pw.button.Button(
        screen, 505, 0, 30, 600, text='<->',
        fontSize=20, margin=20,
        inactiveColour=(255, 204, 204),
        hoverColour=(255,229,204),
        pressedColour=(0, 0, 0),
        onClick=lambda: IncreaseWindow())

    Button.draw()
    pw.update(events)

def DisplayMessage(Message, Interval, Color):
    '''
    General function to display messages on the screen given
        a string "message"
        a interval how long the message should be displayed
        a color the message should be displayed in
    '''
    global grid, complete_grid, counter, original_grid

    screen.blit(a_font.render(Message, True, Color), (545, 540))
    pygame.display.update()
    pygame.time.delay(Interval)
    screen.fill((255, 255, 255))
    DrawModes()
    DrawExtendButton()
    #DrawSolveButton()


def SetGridMode(Mode):
    '''
    Setting up a mode depending on input
    -> daily sudoku, or different difficulties are possible
    reset all the necessary variables after
    '''
    global grid, complete_grid, counter, original_grid, start_time, Fault_Counter, IsSolving, hint_counter
    global guesses, IsFault, IsTimer, IsPause, IsHints, paused_time, pause_start
    screen.fill((255, 255, 255))
    DrawModes()
    DrawExtendButton()
    #DrawSolveButton()
    if Mode == 0:
        grid, complete_grid = GenerateDailySudoku()

    elif Mode == 1:  # For easy mode
        grid, complete_grid = GenerateSudoku(40, False)

    elif Mode == 2:  # For average mode
        grid, complete_grid = GenerateSudoku(32, False)

    elif Mode == 3:  # For hard mode
        grid, complete_grid = GenerateSudoku(25, False)

    original_grid = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            original_grid[i][j] = grid[i][j]
    IsSolving = False
    guesses = [[set() for _ in range(9)] for _ in range(9)]
    Fault_Counter = 0

    start_time = pygame.time.get_ticks()
    paused_time = 0
    pause_start = 0

    hint_counter = 0
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
def SmartNotesChange():
    global IsSmartNotes
    if IsSmartNotes == True:
        IsSmartNotes = False
    else:
        IsSmartNotes = True

def PauseChange():
    '''
    Add the paused time so we can subtract that from the time since it started to get the time the puzzles was being played
    '''
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
        pygame.draw.line(screen, (0, 0, 0), (i * inc, 0), (i * inc, width_sudoku - 4), width)  # vertical
        pygame.draw.line(screen, (0, 0, 0), (0, i * inc), (width_sudoku - 4, i * inc), width)  # horizontal


def IncreaseWindow():
    global IsExtended, screen, width_screen, height_screen
    if IsExtended:
        width_screen = 890
        screen = pygame.display.set_mode((width_screen, height_screen), RESIZABLE)
        screen.fill((255, 255, 255))
        DrawModes()
        IsExtended = False
    else:
        width_screen = 535
        screen = pygame.display.set_mode((width_screen, height_screen), RESIZABLE)
        screen.fill((255, 255, 255))
        IsExtended = True


def HandleEvents():
    '''
    Inputs being verified, either mouse position or keyboard input
    '''
    global IsRunning, grid, complete_grid,  x, y, UserValue, GuessValue, counter, original_grid, IsSolving
    events = pygame.event.get()
    for event in events:
        # Quit the game window
        if event.type == pygame.QUIT:
            SaveFile()
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
                if event.key == pygame.K_l:
                    SmartNotesChange()
                if event.key == pygame.K_g:
                    CheckAndDraw()
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


    DrawExtendButton()
    #DrawSolveButton()



def DrawUserValue():
    '''
    Draw input value if its right and in an empty cell, else red popup that it was wrong
    If it was wrong and faults are wrong, counting those up, in case we have too many faults, we reset the puzzle
    Redraw new counter?
    '''
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
                        screen.blit(time_surface, (875, 130))
                    SaveFile()


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

                for i in range(9):
                    text = a_font.render(str(i + 1), True, (0, 0, 0))
                    screen.blit(text, (i * inc + 18, 510))
                    text = b_font.render(str(counter[i]), True, (0, 0, 0))
                    screen.blit(text, (i * inc + 18, 550))

                UserValue = 0


def Faults():
    '''
    Draw counting faults next to the settings
    '''
    global Fault_Counter, IsFault
    if IsFault:
        fault_string = str(Fault_Counter)+"/3"
        font = pygame.font.SysFont(None, 30)
        time_surface = font.render(fault_string, True, (0, 0, 0))

        pygame.draw.rect(screen, (255,255,255), (760, 180, 70, 25))
        screen.blit(time_surface, (760, 180))

def Hints():
    '''
    Draw hint counter
    '''
    global hint_counter
    pygame.draw.rect(screen, (255, 255, 255), (760, 255, 70, 25))

    font = pygame.font.SysFont(None, 30)
    hint_text = str('Used ')+str(hint_counter)
    hint_surface = font.render(hint_text, True, (0, 0, 0))
    screen.blit(hint_surface, (760, 255))

def DrawSmartNotes():
    '''
    Draw in settings if smart notes are on or not
    '''
    global IsSmartNotes
    AttributeFont = pygame.font.SysFont("times", 20)
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    font = pygame.font.SysFont(None, 30)

    pygame.draw.rect(screen, (255, 255, 255), rect=(760, 230, 80, 20))
    if IsSmartNotes:
        screen.blit(font.render("On", True, (0, 0, 0)), (760, 230))
    else:
        screen.blit(font.render("Off", True, (0, 0, 0)), (760, 230))


def Timer():
    '''
    Draw timer if currently solving (not done with a sudoku) and not paused
    '''
    global IsTimer, elapsed_ms
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

                pygame.draw.rect(screen, (255,255,255), (760,155,100,100))
                screen.blit(time_surface, (760, 155))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (760, 155, 100, 100))
    else:
        pass

def SaveFile():
    global width_screen, height_screen, width_sudoku, screen, inc, a_font, b_font, c_font
    global start_time, paused_time, pause_start, elapsed_ms
    global grid, complete_grid, original_grid, guesses, counter
    global x, y, UserValue, GuessValue,  hint_counter
    global IsRunning, IsSolving, IsFault, IsTimer, IsPause, IsHints, IsSmartNotes, IsExtended, Fault_Counter

    shelfFile = shelve.open('save')
    shelfFile["width_sudoku"] = width_sudoku
    shelfFile["height_screen"] = height_screen
    shelfFile["width_screen"] = width_screen
    shelfFile['start_time'] =  start_time
    shelfFile['paused_time'] = paused_time
    shelfFile['pause_start'] = pause_start
    shelfFile['grid'] = grid
    shelfFile['complete_grid'] = complete_grid
    shelfFile['original_grid'] = original_grid
    shelfFile['guesses'] = guesses
    shelfFile['counter'] = counter
    shelfFile['hint_counter'] = hint_counter
    shelfFile['IsRunning'] = IsRunning
    shelfFile['IsSolving'] = IsSolving
    shelfFile['IsFault'] = IsFault
    shelfFile['IsTimer'] = IsTimer
    shelfFile['IsPause'] = IsPause
    shelfFile['IsHints'] = IsHints
    shelfFile['IsExtended'] = IsExtended
    shelfFile['Fault_Counter'] = Fault_Counter
    shelfFile['elapsed_ms'] = elapsed_ms
    shelfFile['IsSmartNotes'] = IsSmartNotes

    shelfFile.close()

def LoadFile():
    global width_screen, height_screen, width_sudoku, screen, inc, a_font, b_font, c_font
    global start_time, paused_time, pause_start, elapsed_ms
    global grid, complete_grid, original_grid, guesses, counter
    global x, y, UserValue, GuessValue, hint_counter
    global IsRunning, IsSolving, IsFault, IsTimer, IsPause, IsHints, IsSmartNotes, IsExtended, Fault_Counter

    width_screen = 880
    width_sudoku = 500
    height_screen = 600
    pygame.font.init()
    screen = pygame.display.set_mode((width_screen, height_screen), RESIZABLE)  # Window size
    screen.fill((255, 255, 255))
    pygame.display.set_caption("SudokuApp")
    a_font = pygame.font.SysFont("times", 30, "bold")  # Different fonts to be used
    b_font = pygame.font.SysFont("times", 15, "bold")
    c_font = pygame.font.SysFont("times", 30, False)

    inc = width_sudoku // 9  # Screen size // Number of boxes = each increment
    x = 0
    y = 0
    UserValue = 0
    GuessValue = 0
    try:
        shelfFile = shelve.open('save')
        start_time = -shelfFile['elapsed_ms']
        paused_time = shelfFile['paused_time']
        pause_start = shelfFile['pause_start']
        grid = shelfFile['grid']
        complete_grid = shelfFile['complete_grid']
        original_grid = shelfFile['original_grid']
        guesses = shelfFile['guesses']
        counter = shelfFile['counter']
        hint_counter = shelfFile['hint_counter']
        IsRunning = shelfFile['IsRunning']
        IsSolving = shelfFile['IsSolving']
        IsFault = shelfFile['IsFault']
        IsTimer = shelfFile['IsTimer']
        IsPause = shelfFile['IsPause']
        IsHints = shelfFile['IsHints']
        IsSmartNotes = shelfFile['IsSmartNotes']
        IsExtended = shelfFile['IsExtended']
        Fault_Counter = shelfFile['Fault_Counter']
        #elapsed_ms = shelfFile['elapsed_ms']
        shelfFile.close()

    except:
        grid, complete_grid = GenerateSudoku(30, False)
        original_grid = [[0 for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                original_grid[i][j] = grid[i][j]
        IsRunning = True
        IsSolving = False
        guesses = [[set() for i in range(9)] for j in range(9)]
        IsFault = False
        IsTimer = True
        IsPause = False
        IsHints = True
        IsSmartNotes = True
        IsExtended = True
        Fault_Counter = 0

        elapsed_ms = 0
        start_time = pygame.time.get_ticks()
        paused_time = 0
        pause_start = 0

        hint_counter = 0
        counter = CheckCounter()

def InitializeComponent():
    '''
    Start the game
    '''
    global grid, complete_grid, counter, original_grid
    DrawGrid()
    DrawSelectedBox()
    DrawModes()
    DrawExtendButton()
    #DrawSolveButton()
    pygame.display.update()


def GameThread():
    '''
    Game Loop, drawing whole surface every time
    '''
    global grid, complete_grid, counter, original_grid, start_time
    LoadFile()
    InitializeComponent()

    pygame.init()

    while IsRunning:
        HandleEvents()
        DrawGrid()
        counter = CheckCounter()
        DrawCounter()
        DrawSelectedBox()
        DrawUserValue()


        Timer()
        DrawGuesses()
        DrawHints()
        DrawPause()
        DrawSmartNotes()
        Faults()
        Hints()
        Pause()
        pygame.display.update()


def CheckCounter():
    '''
    Count how many times each digit is in the grid
    '''
    global grid, complete_grid, counter, original_grid
    counter = [0 for i in range(9)]
    for i in range(9):
        for j in range(9):
            if grid[i][j] > 0:
                counter[grid[i][j]-1] += 1
    return counter


def main():
    '''
    Main function to start the game
    Global variables:
    width screen, height_screen, screen, inc    -> width, height and general surface, inc is width // 9 for line placements
    a_font, b_font, c_font                      -> different fonts for bolt / not bolt, and different sizes
    x, y                                        -> placement in the grid
    start_time, pause_start, paused_time        -> for timer
    UserValue, GuessValue                       -> Inputs as notes or actual digits
    grid, complete_grid, original_grid          -> grid (current grid), complete_grid (solution), original grid (start grid)
    guesses, counter                            -> guesses (notes in the current grid), counter (counting how many 1s, 2s,... there are currently)
    hint_counter, Fault_Counter                 -> Counting the hints and faults in the current puzzle
    IsRunning, IsSolving                        -> IsRunning for game loop, IsSolving false once u finish a puzzle until u start a new one
    IsFault, IsTimer,IsPuase,IsHints            -> Changing settings
    '''

    global width_sudoku, height_screen, screen, inc, a_font, b_font, c_font
    global start_time, paused_time, pause_start, elapsed_till_now
    global grid, complete_grid, original_grid, guesses, counter
    global x, y, UserValue, GuessValue,  hint_counter
    global IsRunning, IsSolving, IsFault, IsTimer, IsPause, IsHints, IsSmartNotes, IsExtended, Fault_Counter



    GameThread()



if __name__ == '__main__':
    main()