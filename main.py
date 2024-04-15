import threading
import time
import random
import curses
# import mathplotlib
from actors import Worm as Worm
from actors import Bird as Bird
from actors import Tree as Tree
from enum import Enum

# TREE_STATE = Enum('TREE', 'WORM', 'BIRD', 'WORM_BIRD')


class World:
    # actors: [Worm, Bird, Tree]
    # size: (int, int)
    # screen: curses.window
    #

    def __init__(self, x_size=50, y_size=30):
        self.x_size = x_size
        self.y_size = y_size
        self.sim_over = False

        self.map = [[" " for _ in range(self.x_size)] for _ in range(self.y_size)]

    def __str__(self):
        map_string = "#" * (self.x_size + 2) + '\n'

        for row in self.map:
            map_string += "#"
            for cell in row:
                map_string += cell
            map_string += "#\n"

        map_string += "#" * (self.x_size + 2) + '\n'
        return map_string

    def end(self):
        self.sim_over = True


def keyboard_controller(world, window: curses.window):
    while not world.sim_over:
        char = window.getch()
        if char == curses.KEY_F1:
            world.end()


def run(window):
    world = World()

    keyboard_listener = threading.Thread(target=keyboard_controller, args=(world, window))
    keyboard_listener.start()

    while not world.sim_over:
        window.clear()
        window.insstr(0, 0, str(world))
        window.refresh()
        time.sleep(0.2)

    keyboard_listener.join()


if __name__ == "__main__":
    curses.wrapper(run)
