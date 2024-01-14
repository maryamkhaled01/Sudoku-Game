import random
import numpy as np
import time
import copy
import pygame as pg
from Constants import *
import Cell
import queue 
import button

######################################################################################################
pg.init()
window=pg.display.set_mode(WINDOW_SIZE)
pg.display.set_caption("Sudoko Game")
myfont=pg.font.SysFont('Comic Sans Ms',60)

solve_img = pg.image.load('solve.png').convert_alpha()
clear_img = pg.image.load('clear.png').convert_alpha()
generate_img = pg.image.load('generate.png').convert_alpha()
enter_img = pg.image.load('enter.png').convert_alpha()

generate_button = button.Button(CUBE_SIZE*11.5,CUBE_SIZE*0.5,generate_img,1.5)
solve_button = button.Button(CUBE_SIZE*11.5,CUBE_SIZE*2,solve_img,1.5)
clear_button = button.Button(CUBE_SIZE*11.5,CUBE_SIZE*3.5,clear_img,1.5)
enter_button = button.Button(CUBE_SIZE*11.5,CUBE_SIZE*5,enter_img,1.5)


cells = []

######################################################################################################

queue = queue.Queue()
stepCount = 0

# Iinitial Domain Reduction
def init_domains(grid):
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            cell = Cell.Cell(i,j)
            if grid[i][j] != 0:
                cell.domain = [grid[i][j]]
            row.append(cell)
        cells.append(row)

def intit_queue(grid):
    global queue
    init_domains(grid)
    for i in range(GRID_SIZE):
        addrowarcs(i)
        addcolarcs(i)
        addboxarcs(i)

def addrowarcs(row):
    global queue
    for i in range(GRID_SIZE - 1):
       for j in range(i+1, GRID_SIZE):
            queue.put((cells[row][i], cells[row][j]))
            queue.put((cells[row][j], cells[row][i]))

def addcolarcs(col):
    global queue
    for i in range(GRID_SIZE - 1):
       for j in range(i+1,GRID_SIZE):
            queue.put((cells[i][col], cells[j][col]))
            queue.put((cells[j][col], cells[i][col]))

def addboxarcs(box):
    global queue
    boxcells = []
    for i in range(GRID_SIZE):
       for j in range(GRID_SIZE):
            if cells[i][j].box == box:
                boxcells.append(cells[i][j])
    for i in range(len(boxcells) - 1):  
       for j in range(i+1, len(boxcells)):
            queue.put((boxcells[i], boxcells[j]))
            queue.put((boxcells[j], boxcells[i]))

def add_neighbours_arcs_except_y(x, y):
    global queue
    # add arcs with nodes in the same col
    for i in range(GRID_SIZE):
        if i != x.col and cells[x.row][i] != y:
            queue.put((cells[x.row][i], x))

    # add arcs with nodes in the same col
    for i in range(GRID_SIZE):
        if i != x.row and cells[i][x.col] != y:
            queue.put((cells[i][x.col], x))

    # add arcs with nodes in the same box
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if cells[i][j].box == x.box and i != x.row and j != x.col and cells[i][j] != y:
                queue.put((cells[i][j], x))
    
# AC-3 algorithm 
def ac3():
    global queue
    while not queue.empty():
        cell1, cell2 = queue.get()
        if revise(cell1, cell2):
            if len(cell1.domain) == 0:
                return False
            add_neighbours_arcs_except_y(cell1, cell2)
    return True      

def revise(cell1, cell2):
    global queue
    global stepCount
    revised = False
    for x in cell1.domain:
        if (x in cell2.domain) and (len(cell2.domain)==1): # if there is no allowed y for x
            stepCount += 1
            # print(f'Step {stepCount}:\n Queue Size: {queue.qsize()}\n Arc: {cell1.print_cell()} -> {cell2.print_cell()}\n Domains: {cell1.domain} -> {cell2.domain}\n Remove ({x}) From {cell1.print_cell()}')
            cell1.domain.remove(x)
            # print(f' New Domain: {cell1.domain}\n')
            revised = True
    return revised

def find_empty2(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return cells[i][j]
    return None

def backtracking_ac3(grid):
    intit_queue(grid)
    find = mrv(grid)
    # If assignment is complete
    if not find:
        return True
    # Select-Unassigned Variable
    cell = find

    # For each value in Order_Domain_Values
    if ac3():
        for x in cell.domain:
            # If value is consistent
            if isvalid_pro(grid,cell.row, cell.col,x):
                grid[cell.row][cell.col] = x
                if backtracking_ac3(grid):
                    return True
                grid[cell.row][cell.col] = 0

    return False
######################################################################################################

def place(grid,row,col, val):  
            grid_temp=copy.deepcopy(grid)
            if grid_temp[row][col] == 0 and isvalid_pro(grid,row,col,val):
                grid_temp[row][col]=val
                if  backtracking_ac3(grid_temp):
                    grid[row][col]=val
                    return True
            else:
                return False
def mrv(grid):
    global cells 
    find = find_empty2(grid)
    # If assignment is complete
    if  find is not None:
        # Select-Unassigned Variable
        cell = find
        domain_size=len(cell.domain)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] == 0:
                    if len(cells[i][j].domain) < domain_size:
                        cell=cells[i][j]
        return cell    
    else:
        return False  

def solve_gui(grid):
    intit_queue(grid)
    find = mrv(grid)
    # If assignment is complete
    if not find:
        return True
    # Select-Unassigned Variable
    cell = find
    row =cell.row
    col =cell.col
    pg.draw.rect(window, RED, (CUBE_SIZE*0.5+col*CUBE_SIZE,CUBE_SIZE*0.5+row*CUBE_SIZE, CUBE_SIZE ,CUBE_SIZE), 3)
    pg.display.update()
    # For each value in Order_Domain_Values
    if ac3():
        for x in cell.domain:
            pg.draw.rect(window, WHITE, (CUBE_SIZE*0.5+col*CUBE_SIZE+7,CUBE_SIZE*0.5+row*CUBE_SIZE+7, CUBE_SIZE-15,CUBE_SIZE-15))
            pg.draw.rect(window, RED, (CUBE_SIZE*0.5+col*CUBE_SIZE,CUBE_SIZE*0.5+row*CUBE_SIZE, CUBE_SIZE ,CUBE_SIZE), 3)
            value=myfont.render(str(int(x)),True,BLACK)
            window.blit(value, (col*CUBE_SIZE+CUBE_SIZE*0.5+15,row*CUBE_SIZE+CUBE_SIZE*0.5-10))
            pg.display.update()
            # If value is consistent
            if isvalid_pro(grid,cell.row, cell.col,x):
                pg.draw.rect(window, GREEN, (CUBE_SIZE*0.5+col*CUBE_SIZE,CUBE_SIZE*0.5+row*CUBE_SIZE, CUBE_SIZE ,CUBE_SIZE), 3)
                pg.display.update()
                grid[cell.row][cell.col] = x
                if solve_gui(grid):
                    return True
                grid[cell.row][cell.col] = 0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return    
        pg.draw.rect(window, WHITE, (CUBE_SIZE*0.5+col*CUBE_SIZE+7,CUBE_SIZE*0.5+row*CUBE_SIZE+7, CUBE_SIZE-15,CUBE_SIZE-15))
        pg.draw.rect(window, RED, (CUBE_SIZE*0.5+col*CUBE_SIZE,CUBE_SIZE*0.5+row*CUBE_SIZE, CUBE_SIZE ,CUBE_SIZE), 3)
        pg.display.update()
        #pg.time.delay(100)

    return False

def clean_screen(grid,temp_grid,temp_grid2,selected,row,col,key,text,puzz):
    window.fill(WHITE)
    for i in range(0,10):
        if(i%3==0):
            pg.draw.line(window,BLACK,(CUBE_SIZE*0.5+CUBE_SIZE*i,VERTICAL_Y1),(CUBE_SIZE*0.5+CUBE_SIZE*i,VERTICAL_Y2),5) #vertical line
            pg.draw.line(window,BLACK,(HORIZONTAL_X1,CUBE_SIZE*0.5+CUBE_SIZE*i),(HORIZONTAL_X2,CUBE_SIZE*0.5+CUBE_SIZE*i),5) #horizontal line
        pg.draw.line(window,BLACK,(CUBE_SIZE*0.5+CUBE_SIZE*i,VERTICAL_Y1),(CUBE_SIZE*0.5+CUBE_SIZE*i,VERTICAL_Y2),2) #vertical line
        pg.draw.line(window,BLACK,(HORIZONTAL_X1,CUBE_SIZE*0.5+CUBE_SIZE*i),(HORIZONTAL_X2,CUBE_SIZE*0.5+CUBE_SIZE*i),2) #horizontal line
    
    if selected :
        if key!=None and grid[row][col]==0:
            if puzz:
                temp_grid[row][col]=key
                key=None
            else:
                temp_grid2[row][col]=key
        pg.draw.rect(window, RED, (CUBE_SIZE*0.5+col*CUBE_SIZE,CUBE_SIZE*0.5+row*CUBE_SIZE, CUBE_SIZE ,CUBE_SIZE), 3)

    for i in range(0,GRID_SIZE):
        for j in range(0,GRID_SIZE):
            if(grid[i][j]!=0 ):
                value=myfont.render(str(int(grid[i][j])),True,BLACK)
                window.blit(value, (j*CUBE_SIZE+CUBE_SIZE*0.5+15,i*CUBE_SIZE+CUBE_SIZE*0.5-10))

    for i in range(0,GRID_SIZE):
        for j in range(0,GRID_SIZE):
            if(temp_grid[i][j]!=0 ):
                value=myfont.render(str(int(temp_grid[i][j])),True,GREY)
                window.blit(value, (j*CUBE_SIZE+CUBE_SIZE*0.5+15,i*CUBE_SIZE+CUBE_SIZE*0.5-10))

    for i in range(0,GRID_SIZE):
        for j in range(0,GRID_SIZE):
            if(temp_grid2[i][j]!=0 ):
                value=myfont.render(str(int(temp_grid2[i][j])),True,BLUE)
                window.blit(value, (j*CUBE_SIZE+CUBE_SIZE*0.5+15,i*CUBE_SIZE+CUBE_SIZE*0.5-10))            
    
    if text==1:
        value=myfont.render(str("Loading..."),True,BLACK)
        window.blit(value, (CUBE_SIZE*11.5,CUBE_SIZE*8))
    elif text==2:
        value=myfont.render(str("Solvable."),True,BLACK)
        window.blit(value, (CUBE_SIZE*11.5,CUBE_SIZE*8))
    elif text==3: 
        value=myfont.render(str("Not Solvable."),True,BLACK)
        window.blit(value, (CUBE_SIZE*11,CUBE_SIZE*8))   
        

def play():
    selected=False
    key=None
    row=-100
    col=-100
    solved =False
    text=0
    win=0
    puzz=False
    valid =True
    global cells
    global stepCount
    global queue
    grid =np.zeros((GRID_SIZE, GRID_SIZE))
    temp_grid =np.zeros((GRID_SIZE, GRID_SIZE))
    temp_grid2 =np.zeros((GRID_SIZE, GRID_SIZE))
    clean_screen(grid,temp_grid,temp_grid2,selected,row,col,key,text,puzz) 
    pg.display.update()
    while True :
        clean_screen(grid,temp_grid,temp_grid2,selected,row,col,key,text,puzz) 

        if generate_button.draw(window) == 1:
            valid=True
            text=1
            clean_screen(grid,temp_grid,temp_grid2,selected,row,col,key,text,puzz) 
            pg.display.update()
            temp_grid =np.zeros((GRID_SIZE, GRID_SIZE))
            temp_grid2 =np.zeros((GRID_SIZE, GRID_SIZE))
            start_time = time.time() 
            grid =generate()
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time} seconds")
            cells = [] 
            text=0
            solved=False
            puzz=True
        
        if solve_button.draw(window) == 1 and not solved and puzz:
            while not queue.empty():
                queue.get()
            cells=[]
            stepCount=0
            text=1
            temp_grid =np.zeros((GRID_SIZE, GRID_SIZE))
            temp_grid2 =np.zeros((GRID_SIZE, GRID_SIZE))
            clean_screen(grid,temp_grid,temp_grid2,selected,row,col,key,text,puzz) 
            pg.display.update()  
            start_time = time.time() 
            grid_temp=copy.deepcopy(grid)
            
            if backtracking_ac3(grid_temp):
                grid=copy.deepcopy(grid_temp)
                solved = True
            text=0
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time} seconds")
           

        if clear_button.draw(window) == 1:
            valid=True
            if puzz:
                temp_grid =np.zeros((GRID_SIZE, GRID_SIZE))
            else:
                temp_grid2 =np.zeros((GRID_SIZE, GRID_SIZE))
            if solved:
                temp_grid =np.zeros((GRID_SIZE, GRID_SIZE))
                temp_grid2 =np.zeros((GRID_SIZE, GRID_SIZE))
                grid =np.zeros((GRID_SIZE, GRID_SIZE))
                puzz=False

            solved = False
            cells = [] 
            text=0

        if enter_button.draw(window) and not np.all(temp_grid2 == 0):
            if isvalid_puz(temp_grid2):
                grid=copy.deepcopy(temp_grid2)
                temp_grid2 =np.zeros((GRID_SIZE, GRID_SIZE))
                puzz=True
                valid = True
            else:
                valid=False

        if not valid:  
            value=myfont.render(str("Invalid puzzle."),True,BLACK)
            window.blit(value,(CUBE_SIZE*10.5,CUBE_SIZE*7))

        if win== 1:
            value=myfont.render(str("Success"),True,BLACK)
            window.blit(value,(CUBE_SIZE*11.5,CUBE_SIZE*7))
        elif win==-1:
            value=myfont.render(str("Wrong"),True,BLACK)
            window.blit(value, (CUBE_SIZE*11.5,CUBE_SIZE*7))
            

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return

            if event.type == pg.MOUSEBUTTONDOWN and not solved:
                key=None
                pos = pg.mouse.get_pos()
                win=0
                if pos[0]>HORIZONTAL_X1 and pos[0] <HORIZONTAL_X2  and pos[1] > VERTICAL_Y1 and pos[1] < VERTICAL_Y2:
                    col = (int) (pos[0]-CUBE_SIZE*0.5) // CUBE_SIZE
                    row = (int) (pos[1]-CUBE_SIZE*0.5) // CUBE_SIZE
                    
                    selected=True
                    clean_screen(grid,temp_grid,temp_grid2,selected,row,col,key,text,puzz) 
                else:
                    selected=False
                    clean_screen(grid,temp_grid,temp_grid2,selected,row,col,key,text,puzz) 
                    pg.display.update()    

            if event.type == pg.KEYDOWN:
                win=0
                if event.key == pg.K_1:
                    key = 1
                if event.key == pg.K_2:
                    key = 2
                if event.key == pg.K_3:
                    key = 3
                if event.key == pg.K_4:
                    key = 4
                if event.key == pg.K_5:
                    key = 5
                if event.key == pg.K_6:
                    key = 6
                if event.key == pg.K_7:
                    key = 7
                if event.key == pg.K_8:
                    key = 8
                if event.key == pg.K_9:
                    key = 9
                if event.key == pg.K_KP1:
                    key = 1
                if event.key == pg.K_KP2:
                    key = 2
                if event.key == pg.K_KP3:
                    key = 3
                if event.key == pg.K_KP4:
                    key = 4
                if event.key == pg.K_KP5:
                    key = 5
                if event.key == pg.K_KP6:
                    key = 6
                if event.key == pg.K_KP7:
                    key = 7
                if event.key == pg.K_KP8:
                    key = 8
                if event.key == pg.K_KP9:
                    key = 9    
                if event.key == pg.K_DELETE:
                    key = 0    
                if event.key == pg.K_RETURN and puzz==True:
                    text=1
                    clean_screen(grid,temp_grid,temp_grid2,selected,row,col,key,text,puzz) 
                    pg.display.update()
                    start_time = time.time()
                    if place(grid,row,col,temp_grid[row][col]):
                        win=1  
                    else:
                        win=-1
                    temp_grid[row][col]=0   
                    text=0
                    clean_screen(grid,temp_grid,temp_grid2,selected,row,col,key,text,puzz) 
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f"Elapsed time: {elapsed_time} seconds")
                    pg.display.update()
        pg.display.update()    
                        
 
play()
