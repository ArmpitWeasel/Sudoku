import pygame
from Solver import solve, valid
import time
pygame.font.init()


class Grid:
    board = [
    [0,0,9,0,4,0,0,0,0],
    [0,0,0,0,0,5,3,1,0],
    [0,6,1,0,0,8,0,5,0],
    [0,0,5,4,0,0,2,0,3],
    [0,1,0,0,0,7,0,0,8],
    [0,8,0,0,0,0,7,6,0],
    [3,0,6,0,1,9,4,0,0],
    [7,0,0,0,0,0,0,0,0],
    [0,0,4,0,5,0,6,2,7]
    ]

    def __init__(pers, rows, cols, width, height, win):
        pers.rows = rows
        pers.cols = cols
        pers.cubes = [[Cube(pers.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        pers.width = width
        pers.height = height
        pers.model = None
        pers.update_model()
        pers.selected = None
        pers.win = win

    def update_model(pers):
        pers.model = [[pers.cubes[i][j].value for j in range(pers.cols)] for i in range(pers.rows)]

    def place(pers, val):
        row, col = pers.selected
        if pers.cubes[row][col].value == 0:
            pers.cubes[row][col].set(val)
            pers.update_model()

            if valid(pers.model, val, (row,col)) and pers.solve():
                return True
            else:
                pers.cubes[row][col].set(0)
                pers.cubes[row][col].set_temp(0)
                pers.update_model()
                return False

    def sketch(pers, val):
        row, col = pers.selected
        pers.cubes[row][col].set_temp(val)

    def draw(pers):
        
        gap = pers.width / 9
        for i in range(pers.rows+1):
            if i % 3 == 0 and i != 0:
                thickboi = 4
            else:
                thickboi = 1
            pygame.draw.line(pers.win, (0,0,0), (0, i*gap), (pers.width, i*gap), thickboi)
            pygame.draw.line(pers.win, (0, 0, 0), (i * gap, 0), (i * gap, pers.height), thickboi)

        # Draw Cubes
        for i in range(pers.rows):
            for j in range(pers.cols):
                pers.cubes[i][j].draw(pers.win)

    def select(pers, row, col):
        # Reset all other
        for i in range(pers.rows):
            for j in range(pers.cols):
                pers.cubes[i][j].selected = False

        pers.cubes[row][col].selected = True
        pers.selected = (row, col)

    def clear(pers):
        row, col = pers.selected
        if pers.cubes[row][col].value == 0:
            pers.cubes[row][col].set_temp(0)

    def click(pers, pos):

        if pos[0] < pers.width and pos[1] < pers.height:
            gap = pers.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(pers):
        for i in range(pers.rows):
            for j in range(pers.cols):
                if pers.cubes[i][j].value == 0:
                    return False
        return True

    def solve(pers):
        find = find_empty(pers.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(pers.model, i, (row, col)):
                pers.model[row][col] = i

                if pers.solve():
                    return True

                pers.model[row][col] = 0

        return False

    def solve_gui(pers):
        pers.update_model()
        find = find_empty(pers.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(pers.model, i, (row, col)):
                pers.model[row][col] = i
                pers.cubes[row][col].set(i)
                pers.cubes[row][col].draw_change(pers.win, True)
                pers.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if pers.solve_gui():
                    return True

                pers.model[row][col] = 0
                pers.cubes[row][col].set(0)
                pers.update_model()
                pers.cubes[row][col].draw_change(pers.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(pers, value, row, col, width, height):
        pers.value = value
        pers.temp = 0
        pers.row = row
        pers.col = col
        pers.width = width
        pers.height = height
        pers.selected = False

    def draw(pers, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = pers.width / 9
        x = pers.col * gap
        y = pers.row * gap

        if pers.temp != 0 and pers.value == 0:
            text = fnt.render(str(pers.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(pers.value == 0):
            text = fnt.render(str(pers.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if pers.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(pers, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = pers.width / 9
        x = pers.col * gap
        y = pers.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(pers.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(pers, val):
        pers.value = val

    def set_temp(pers, val):
        pers.temp = val


def find_empty(su):
    for i in range(len(su)):
        for j in range(len(su[0])):
            if su[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid(su, num, pos):
    # Check row
    for i in range(len(su[0])):
        if su[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(su)):
        if su[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if su[i][j] == num and (i,j) != pos:
                return False

    return True


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw()


def format_time(sex):
    sec = sex%60
    minute = sex//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game Over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
