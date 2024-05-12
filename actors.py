import threading
import time
import random


class Tree:
    def __init__(self, position: (int, int)):
        self.position = position
        self.alive = True
        self.hp = 100
        self.fruits = 5
        self.lock = threading.Lock()

    def __str__(self):
        return 'T'

    def eat(self):
        if (self.alive and self.hp < 100):
            self.hp += 5

    def fruit_create(self):
        if (self.alive and self.hp > 60 and self.fruits < 10):
            with self.lock:
                self.fruits += 1


class Worm:

    def __init__(self, position: (int, int), x_size, y_size):
        self.alive = True
        self.position = position
        self.fatness = 10
        self.x_size = x_size
        self.y_size = y_size
        self.lock = threading.Lock()

    def __str__(self):
        return '-'

    def move(self):
        while True:
            new_position = (self.position[0]+random.choice([-1, 0, 1]),
                            self.position[1]+random.choice([-1, 0, 1]))
            if 0 <= new_position[0] < self.x_size and 0 <= new_position[1] < self.y_size:
                break
        self.position = new_position
        self.fatness -= 1
        return self.position

    def eat(self, t: Tree):
        chance = random.randint(0, 100)
        if self.fatness < 100:
            with t.lock:
                t.hp -= 10
                self.fatness += 5
                if t.fruits > 0 and chance > 50:
                    t.fruits -= 1
                    self.fatness += 5

    def reproduce(self):
        if self.fatness > 30:
            self.fatness -= 10
            return True
        return False


class Bird:

    def __init__(self, position: (int, int), x_size, y_size):
        self.position = position
        self.alive = True
        self.hp = 30
        self.reproducable = 5
        self.x_size = x_size
        self.y_size = y_size
        self.seeds = False

    def __str__(self):
        return 'B'

    def move(self):
        while True:
            new_position = (self.position[0]+random.choice([-2, -1, 0, 1, 2]),
                            self.position[1]+random.choice([-2, -1, 0, 1, 2]))
            if 0 <= new_position[0] < self.x_size and 0 <= new_position[1] < self.y_size:
                break
        self.position = new_position
        self.hp -= 5
        if self.reproducable > 0:
            self.reproducable -= 1
        return self.position

    def eat(self, w: Worm):
        if self.hp < 70:
            with w.lock:
                am = random.randint(1, w.fatness)
                w.fatness -= am
                self.hp += am

    def eat_f(self, t: Tree):
        if self.hp < 70:
            with t.lock:
                t.fruits -= 2
                self.hp += 2
                self.seeds = True

    def reproduce(self, b):
        if (self.hp > 60 and b.hp > 60) and (self.reproducable == 0 and b.reproducable == 0):
            self.hp -= 10
            self.reproducable = 30
            with b.lock:
                b.hp -= 10
                b.reproducable = 30
            return True
        return False

    def populate(self):
        chance = random.randint(0, 100)
        if self.seeds and chance > 50:
            self.seeds = False
            if chance > 70:
                return True
        return False
