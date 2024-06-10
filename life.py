import os
import time
import random
import pygame
from pygame.locals import *

ALIVE = True
DEAD = False

WIDTH = 100
HEIGHT = 80

CELL_SIZE = 8

WIN_WIDTH = WIDTH * CELL_SIZE
WIN_HEIGHT = HEIGHT * CELL_SIZE

BLACK = (0,0,0)
GREY = (169,169,169)
GREEN = (0,255,127)

pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

board = []

changes = []


def print_board():
    '''Displays the board'''
    """    
    os.system("cls")
    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            print(f"| {board[i][j]} ", end="")
        print("")
        if i < HEIGHT - 1:
            for i in range(0, WIDTH):
                print("----", end="")
            print("")
    """
    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            if board[i][j] == ALIVE:
                
                pygame.draw.rect(win, GREEN, 
                                 pygame.rect.Rect(
                                    j * CELL_SIZE,
                                    i * CELL_SIZE,
                                    CELL_SIZE,
                                    CELL_SIZE
                                 ))


def check_board() -> bool:
    """
    Checks each cell to see if it dies, grows, or remains.
    <= 1: Dies
    2-3: Remains
    3: Spawns (Empty spaces)
    4+ : Dies

    Returns if game was changed
    """
    changes.clear()

    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            surrounding = 0

            if i == 0:
                kStart = 0
            else:
                kStart = -1

            if j == 0:
                lStart = 0
            else:
                lStart = -1
            
            if i == HEIGHT-1:
                kEnd = 1
            else:
                kEnd = 2

            if j == WIDTH-1:
                lEnd = 1
            else:
                lEnd = 2

            for k in range(kStart, kEnd):
                for l in range(lStart, lEnd):
                    if k == 0 and l == 0:
                        continue
                    if board[i+k][j+l] == ALIVE:
                        surrounding += 1
            
            match surrounding:
                case 2:
                    pass
                case 3:
                    changes.append([i, j, ALIVE])
                case _:
                    changes.append([i, j, DEAD])
    
    for change in changes:
        board[change[0]][change[1]] = change[2]
    
    if len(changes) != 0:
        return True
    return False


def all_dead() -> bool:
    '''Checks if the board is dead'''

    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            if board[i][j] == ALIVE:
                return False
    return True


def display_grid():
    '''Displays the grid'''

    for i in range(1, HEIGHT):
        pygame.draw.line(win, GREY, 
                         (0, i * CELL_SIZE),
                         (WIN_WIDTH, i * CELL_SIZE)
                         )
    
    for j in range(1, WIDTH):
        pygame.draw.line(win, GREY, 
                         
                         (j * CELL_SIZE, 0),
                         (j * CELL_SIZE, WIN_HEIGHT)
                         )
        
def get_index_from_pos(pos : tuple) -> tuple:
    ''''''
    i = None
    j = None

    for k in range(1, HEIGHT):
        if pos[0] < k * CELL_SIZE:
            i = k - 1
            break
    for l in range(1, WIDTH):
        if pos[1] < l * CELL_SIZE:
            j = l - 1
            break

    return i, j


# Initialize board
for i in range(0, HEIGHT):
    board.append([])
    for j in range(0, WIDTH):
        board[i].append(DEAD)


"""
print_board()
time.sleep(0.5)
while not all_dead():
    check_board()
    print_board()
    time.sleep(0.5)
"""


# Initial Displays
win.fill(BLACK)

display_grid()
print_board()

pygame.display.flip()

# Board Setup
run = True
while run:

    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == MOUSEBUTTONDOWN:
            i, j = get_index_from_pos(pos)
            if i != None and j != None:
                board[i][j] = not board[i][j]
                win.fill(BLACK)
                display_grid()
                print_board()
                pygame.display.flip()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
            if event.key == K_KP_ENTER:
                run = False
            if event.key == K_SPACE:
                run = False

        if event.type == pygame.QUIT: 
            run = False

    clock.tick(30)


# If board not setup, do random
if all_dead():
    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            if random.randint(1, 100) < 40:
                board[i][j] = ALIVE


# Run game until all dead
run = True
fps = 2
while run:
    print(fps)
    win.fill(BLACK)

    display_grid()
    run = check_board()
    print_board()

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
            if event.key == K_EQUALS:
                fps += 1
            if event.key == K_MINUS and fps > 1:
                fps -= 1


        if event.type == pygame.QUIT: 
            run = False

    clock.tick(fps)