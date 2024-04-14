import threading
import time
import random
import curses
import mathplotlib
from actors import Worm as Worm
from actors import Bird as Bird
from actors import Tree as Tree
from enum import Enum

TREE_STATE = Enum('TREE', 'WORM', 'BIRD', 'WORM_BIRD')


class World():
    actors: [Worm, Bird, Tree]
    size: (int, int)
    screen: curses.window
