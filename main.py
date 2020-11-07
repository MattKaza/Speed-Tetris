import player
import keyboard
from consts import *
import time

def event_loop(player, sample_speed, fall_speed):      
        last_cycle = time.time()
        while True:
            time.sleep(sample_speed)
            if keyboard.is_pressed('right'):
                player.move_sideways(1)
                print_board(player)
            if keyboard.is_pressed('left'):
                player.move_sideways(-1)
                print_board(player)
            if keyboard.is_pressed('up'):
                player.rotate()
                print_board(player)
            if keyboard.is_pressed('down'):
                player.cycle()
                print_board(player)
                
            if time.time() - last_cycle >= fall_speed:
                last_cycle = time.time()
                player.cycle()
                print_board(player)
                 
def print_board(player):
    for i in reversed(range(DISPLAYED_HEIGHT)):
        print(player.board[i])
    print(SEPARATOR)
            
p = player.Player()
event_loop(p, 0.1, 0.5)