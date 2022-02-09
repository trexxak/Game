import numpy as np
import copy
from numpy import empty, random as zufall

leerzellen = 42
ziffern = list(zufall.permutation(np.array([1,2,3,4,5,6,7,8,9])))
brett = [
    [ziffern[0],-1,ziffern[8],ziffern[2],ziffern[6],-1,ziffern[7],-1,ziffern[1]],
    [-1,ziffern[1],-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,ziffern[2],-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,ziffern[3],-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,ziffern[4],-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,ziffern[5],-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,ziffern[6],-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,ziffern[7],-1],
    [-1,-1,ziffern[3],-1,-1,-1,-1,-1,ziffern[8]],
]

def find_next_empty(puzzle):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c

    return None, None

def is_valid(puzzle, guess, row, col):
    row_vals = puzzle[row]
    if guess in row_vals:
        return False
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start +3):
            if puzzle[r][c] == guess:
                return False
    return True

def solve_sudoku(puzzle):
    row, col = find_next_empty(puzzle)
    if row is None:
        return True
    for guess in range(1,10):
        if is_valid(puzzle,guess,row,col):
            puzzle[row][col] = guess
            if solve_sudoku(puzzle):
                return True
        puzzle[row][col] = -1
    return False

def empty_some(puzzle, empty_cells=leerzellen):
    for i in range(empty_cells):
        zufall.shuffle(ziffern)
        r_wahl = zufall.choice(ziffern)-1
        c_wahl = zufall.choice(ziffern)-1
        check = True
        while check:
            if puzzle[r_wahl][c_wahl] == -1:
                r_wahl = zufall.choice(ziffern)-1
                c_wahl = zufall.choice(ziffern)-1
                continue
            else:
                puzzle[r_wahl][c_wahl] = -1
                check = False
       
def generate_sudoku():
    solve_sudoku(brett)
    brett_2 = copy.deepcopy(brett)
    empty_some(brett)
    return [brett, brett_2]

if __name__ == "__main__":
    solve_sudoku(brett)
    empty_some(brett)
