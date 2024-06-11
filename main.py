import sys
import threading
import time
import random
import curses
import traceback

from plotting import Plot as Plt
from actors import Worm as Worm
from actors import Bird as Bird
from actors import Tree as Tree


class World:
    def __init__(self, x_size=50, y_size=30):
        self.x_size = x_size
        self.y_size = y_size
        self.sim_over = False
        self.trees = {}
        self.worms = {}
        self.birds = {}
        self.lock_map = threading.Lock()
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

    def refresh(self):
        self.map = [[" " for _ in range(self.x_size)] for _ in range(self.y_size)]

        if not self.birds and not self.worms:
            self.sim_over = True
            return

        for worm in list(self.worms):
            if not worm.alive:
                self.worms[worm].join()
                del self.worms[worm]
                continue
            x, y = worm.position
            self.map[y][x] = str(worm)

        for tree in list(self.trees):
            if not tree.alive:
                self.trees[tree].join()
                del self.trees[tree]
                continue
            x, y = tree.position
            self.map[y][x] = str(tree)

        for bird in list(self.birds):
            if not bird.alive:
                self.birds[bird].join()
                del self.birds[bird]
                continue
            x, y = bird.position
            self.map[y][x] = str(bird)

    @staticmethod
    def adjacent_tiles(position: (int,int)):
        return[(position[0]+1, position[1]+1),
               (position[0], position[1]+1),
               (position[0]+1, position[1]),
               (position[0]-1, position[1]-1),
               (position[0]-1, position[1]),
               (position[0], position[1]-1),
               (position[0]-1, position[1]+1),
               (position[0]+1, position[1]-1),]

    def add_worms(self, amount: int):
        for _ in range(amount):
            temp_worm = Worm((random.randint(0, self.x_size - 1), random.randint(0, self.y_size - 1)),
                             self.x_size, self.y_size)
            self.worms[temp_worm] = threading.Thread(target=self.worm_worker, args=(temp_worm,))
            self.worms[temp_worm].start()

    def add_trees(self, amount: int):
        for _ in range(amount):
            temp_tree = Tree((random.randint(0, self.x_size - 1), random.randint(0, self.y_size - 1)))
            self.trees[temp_tree] = threading.Thread(target=self.tree_worker, args=(temp_tree,))
            self.trees[temp_tree].start()

    def add_birds(self, amount: int):
        for _ in range(amount):
            temp_bird = Bird((random.randint(0, self.x_size - 1), random.randint(0, self.y_size - 1)),
                             self.x_size, self.y_size)
            self.birds[temp_bird] = threading.Thread(target=self.bird_worker, args=(temp_bird,))
            self.birds[temp_bird].start()

    def new_worm(self, position: (int, int)):
        temp_worm = Worm(position, self.x_size, self.y_size)
        self.worms[temp_worm] = threading.Thread(target=self.worm_worker, args=(temp_worm,))
        self.worms[temp_worm].start()

    def new_tree(self, position: (int, int)):
        temp_tree = Tree(position)
        self.trees[temp_tree] = threading.Thread(target=self.tree_worker, args=(temp_tree,))
        self.trees[temp_tree].start()

    def new_bird(self, position: (int, int)):
        temp_bird = Bird(position, self.x_size, self.y_size)
        self.birds[temp_bird] = threading.Thread(target=self.bird_worker, args=(temp_bird,))
        self.birds[temp_bird].start()

    def worm_worker(self, worm):
        while worm.alive:
            time.sleep(0.2)
            my_tiles = self.adjacent_tiles(worm.position)
            adjtrees = list(filter(lambda x: x.position in my_tiles, self.trees.keys()))
            if len(adjtrees) > 0:
                worm.eat(adjtrees[0])
                if worm.fatness <= 0:
                    worm.alive = False
                continue
            else:
                worm.move()
            if worm.reproduce():
                x, y = worm.position
                with self.lock_map:
                    if worm.alive:
                        self.new_worm((x, y))
            if worm.fatness <= 0:
                worm.alive = False

    def tree_worker(self, tree):
        while tree.alive:
            time.sleep(1)
            tree.eat()
            tree.fruit_create()

            if tree.hp <= 0:
                tree.alive = False

    def bird_worker(self, bird):
        while bird.alive:
            time.sleep(0.5)
            my_tiles = self.adjacent_tiles(bird.position)
            adjtrees = list(filter(lambda x: x.position in my_tiles, self.trees.keys()))
            adjworms = list(filter(lambda x: x.position in my_tiles, self.worms.keys()))
            adjbirds = list(filter(lambda x: x.position in my_tiles, self.birds.keys()))
            if len(adjworms) > 0:
                if not adjworms[0].lock.locked() and bird.hp < 70:
                    bird.eat(adjworms[0])
                    if bird.hp <= 0:
                        bird.alive = False
                    continue
            if len(adjtrees) > 0:
                if adjtrees[0].fruits > 0 and not adjtrees[0].lock.locked() and bird.hp < 70:
                    bird.eat_f(adjtrees[0])
                else:
                    bird.move()
                    if bird.hp <= 0:
                        bird.alive = False
                    continue
            if len(adjbirds) > 0:
                if bird.reproduce(adjbirds[0]):
                    with self.lock_map:
                        if bird.alive:
                            self.new_bird(bird.position)
                bird.move()
                if bird.hp <= 0:
                    bird.alive = False
                continue
            bird.move()
            if bird.populate():
                with self.lock_map:
                    if bird.alive:
                        self.new_tree(bird.position)
            if bird.hp <= 0:
                bird.alive = False

    def end(self):
        with self.lock_map:
            self.sim_over = True
            for worm, thread in self.worms.items():
                worm.alive = False

            for tree, thread in self.trees.items():
                tree.alive = False

            for bird, thread in self.birds.items():
                bird.alive = False

    def clear(self):
        for worm, thread in self.worms.items():
            thread.join()
        for tree, thread in self.trees.items():
            thread.join()
        for bird, thread in self.birds.items():
            thread.join()

    def dune_worm(self):
        time.sleep(10)
        chance = random.randint(0, 100)
        rx = random.randint(0, self.x_size//2)
        ry = random.randint(0, self.y_size//2)
        check = lambda worker: worker.position[0] in range(self.x_size//2 - rx, self.x_size//2 + rx) and \
                        worker.position[1] in range(self.y_size//2 - ry, self.y_size//2+ry)
        if len(self.worms) > 100 and chance > 90:
            for worm in list(self.worms):
                if check(worm):
                    worm.alive = False
            for tree in list(self.trees):
                if check(tree):
                    tree.alive = False
            for bird in list(self.birds):
                if check(bird):
                    bird.alive = False
            for (x,y) in [(x,y) for x in range(self.x_size//2 - rx, self.x_size//2 + rx ) for y in range(self.y_size//2 - ry, self.y_size//2+ry)]:
                self.map[y][x] = 'X'

def keyboard_controller(world, window: curses.window):
    while not world.sim_over:
        char = window.getch()
        if char == curses.KEY_UP:
            world.end()


def collect(world, plot):
    while not world.sim_over:
        plot.get_data(world, world.worms, world.trees, world.birds)
        time.sleep(0.15)


def run(window):
    try:
        world = World(180, 40)
        plot = Plt()
        world.add_worms(1000)
        world.add_trees(100)
        world.add_birds(50)
        collect_data = threading.Thread(
                target=collect,
                args=(world, plot))
        collect_data.start()
        
        keyboard_listener = threading.Thread(
                target=keyboard_controller, args=(world, window))
        keyboard_listener.start()

        dune = threading.Thread(target=world.dune_worm)
        dune.start()

        while not world.sim_over:
            window.clear()
            window.insstr(0, 0, str(world))
            window.refresh()
            time.sleep(0.1)

            world.refresh()

        keyboard_listener.join()
        collect_data.join()
        dune.join()
        plot.toggle_show()
        world.clear()
        return
    except Exception as e:
        with open("log.txt", 'a') as file:
            file.write(f"{str(''.join(traceback.format_tb(e.__traceback__)))}\t{time.time()}\n")


if __name__ == "__main__":
    try:
        curses.wrapper(run)
        sys.exit()
    except Exception as e:
        with open("log.txt", 'a') as file:
            file.write(f"{str(e.__traceback__.tb_next)}\t{time.time()}\n")
