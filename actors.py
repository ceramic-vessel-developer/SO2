import threading
import time
import random


class Worm():
    position: (int, int)
    fatness: int

    def __init__(self, position: (int, int)):
        self.position = position
        self.fatness = 20

    def __str__(self):
        return '-'

    def move(self):
        self.position = (self.position[0]+random.choice([-1, 0, 1]),
                         self.position[1]+random.choice([-1, 0, 1]))
        self.fatness -= 1
        return self.position

    def eat(self):
        pass

    def reproduce(self):
        pass


class Bird():
    position: (int, int)
    hp: int

    def __init__(self, position: (int, int)):
        self.position = position
        self.hp = 50

    def __str__(self):
        return 'B'

    def move(self):
        self.position = (self.position[0]+random.choice([-1, 0, 1]),
                         self.position[1]+random.choice([-1, 0, 1]))
        self.hp -= 1
        return self.position

    def eat(self):
        pass

    def reproduce(self):
        pass

    def populate(self):
        pass


class Tree():
    position: (int, int)
    hp: int
    fruits: int

    def __init__(self, position: (int, int)):
        self.position = position
        self.hp = 100
        self.fruits = 5

    def __str__(self):
        return 'T'

    def eat(self):
        pass

    def fruit_create(self):
        pass


