import game
import keyboard
from consts import *
import time


def event_loop(player, sample_speed, fall_speed):      
    last_cycle = time.time()
    while True:
        time.sleep(sample_speed)
        if keyboard.is_pressed('right'):
            player.move_sideways(1)
            print_screen(player)
        if keyboard.is_pressed('left'):
            player.move_sideways(-1)
            print_screen(player)
        if keyboard.is_pressed('up'):
            player.rotate()
            print_screen(player)
        if keyboard.is_pressed('down'):
            player.cycle()
            print_screen(player)
        if keyboard.is_pressed('space'):
            player.hard_drop()
            print_screen(player)

        if time.time() - last_cycle >= fall_speed:
            last_cycle = time.time()
            player.cycle()
            print_screen(player)


def draw_board(player):
    board = ['┏' + ('━' * WIDTH * 2) + '┓']
    for i in reversed(range(DISPLAYED_HEIGHT)):
        row = '┃'
        for j in range(WIDTH):
            block = '██' if player.board[i][j] != 0 else ' ·'
            row += block
        row += '┃'
        board.append(row)
    board.append('┗' + ('━' * WIDTH * 2) + '┛')
    return board


def print_screen(player):
    for row in draw_board(player):
        print(row)


p = game.Player()
event_loop(p, 0.1, 0.5)
