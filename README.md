Sudoku Game for fun
2 Versions
  1. with a mathematical approach modelling sudoku as a mixed integer problem and solving it with scip (SudokuMath)
  2. with a recursive approach and backtracking (Sudoku)

To play, open either SudokuGame.py or SudokuGameWithoutMath.py with python or unzip the zip data and open the exe in there.
Main focus on SudokuGame.py, less features in SudokuGameMath.py


Can click on tiles or walk from tile to tile with arrow buttons
Shift + Number to input a note, Number to input a number

Settings:
  - Timer if turned on shows timer counting up
  - Faults if turned on wrong inputs will be counted - at 3 faults game will be lost and you have to start all over again
  - Pause if turned on pauses the game till it continues
  - Options for hints: Solved (give a spot in the grid and a number) or unsolved (only give the spot, not the number)
  - Hint button to find a currently solvable cell with solution strategy to find it (and number if option is on)
  - Load last reset if game crashed

Modes:
  - Daily Puzzle with a random difficulty
  - Easy - Average- Hard: Create sudoku grid with 25/32/40 given digits
