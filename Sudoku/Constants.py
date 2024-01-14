import random
import numpy as np
import copy

GRID_SIZE=9
CUBE_SIZE=80
WINDOW_SIZE=(CUBE_SIZE*16,CUBE_SIZE*10)
DOMAIN=[i for i in range(1,10)]
HORIZONTAL_X1=CUBE_SIZE*0.5
HORIZONTAL_X2=CUBE_SIZE*10-CUBE_SIZE*0.5
VERTICAL_Y1=CUBE_SIZE*0.5
VERTICAL_Y2=CUBE_SIZE*10-CUBE_SIZE*0.5


#COLORS
WHITE=(255,255,255)
BLACK=(0,0,0)
GREY=(217, 217, 217)
RED=(255,0,0)
GREEN = (0,255,0)
BLUE= (0,0,255)

# FONTS
F1 = "Courier New"
F2 = "stylus"
F3 = "arialblack"


def isvalid_pro(grid,row, col, n):
    for i in range(0, 9):
        if grid[row][i] == n or grid[i][col]==n or grid[(3*(row//3)+(i//3))][(3*(col//3)+(i%3))] == n: # Checks for number (n) in X columns
            return False
    
    return True

def isvalid(grid,row, col, n):
    # Check row
    for i in range(GRID_SIZE):
        if i != col and grid[row][i] == n:
            return False

    # Check column
    for i in range(GRID_SIZE):
        if i != row and grid[i][col] == n:
            return False

    # Check 3x3 subgrid
    x0 = (row // 3) * 3
    y0 = (col // 3) * 3
    for i in range(x0, x0 + 3):
        for j in range(y0, y0 + 3):
            if (i != row or j != col) and grid[i][j] == n:
                return False
    return True

def find_empty(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return (i, j)
    return None



def backtracking(grid):
    find = find_empty(grid)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if isvalid_pro(grid,row, col,i):
            grid[row][col] = i
            if backtracking(grid):
                return True
            grid[row][col] = 0

    return False

def generate():
    grid =np.zeros((GRID_SIZE, GRID_SIZE))
    arr=[1,2,3,4,5,6,7,8,9]
    random.shuffle(arr)
    for i in range(0, 7, 3):
        random.shuffle(arr)
        y=0
        for j in range(3):
            for k in range(3):
                grid[i+j][i+k]=arr[y]
                y=y+1  

    backtracking(grid)
    
    empty_cells = 45  # Adjust this number to change the difficulty of the puzzle
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)

    for cell in cells:
        if empty_cells <= 0:
            break
        row, col = cell
        temp = grid[row][col]
        grid[row][col] = 0

        temp_board = copy.deepcopy(grid)
        if backtracking(temp_board):
            empty_cells -= 1
        else:
            grid[row][col] = temp
    return grid

def isvalid_puz(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] !=0:
                
                if not isvalid(grid,i,j,grid[i][j]):
                    return False
    return True 