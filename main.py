import threading
import time
import random
import curses
# from plotting import Plot as Plt
from actors import Worm as Worm
from actors import Bird as Bird
from actors import Tree as Tree


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
        # self.plot = Plt()
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
        with self.lock_map:
            temp_worm = Worm(position, self.x_size, self.y_size)
            self.worms[temp_worm] = threading.Thread(target=self.worm_worker, args=(temp_worm,))
            self.worms[temp_worm].start()

    def new_tree(self, position: (int, int)):
        with self.lock_map:
            temp_tree = Tree(position)
            self.trees[temp_tree] = threading.Thread(target=self.tree_worker, args=(temp_tree,))
            self.trees[temp_tree].start()

    def new_bird(self, position: (int, int)):
        with self.lock_map:
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
                    self.new_bird(bird.position)
                bird.move()
                if bird.hp <= 0:
                    bird.alive = False
                continue
            bird.move()
            if bird.populate():
                self.new_tree(bird.position)
            if bird.hp <= 0:
                bird.alive = False

    def end(self):
        self.sim_over = True
        for worm, thread in self.worms.items(): thread.join()
        for tree, thread in self.trees.items(): thread.join()
        for bird, thread in self.birds.items(): thread.join()

        for worm, thread in self.worms.items():
            worm.alive = False
            del worm
            thread.join()

        for tree, thread in self.trees.items():
            tree.alive = False
            del tree
            thread.join()

        for bird, thread in self.birds.items():
            bird.alive = False
            del bird
            thread.join()


def keyboard_controller(world, window: curses.window):
    while not world.sim_over:
        char = window.getch()
        if char == curses.KEY_UP:
            world.end()
        # if char == curses.KEY_DOWN:
          #  world.plot.toggle_show()


def run(window):
    world = World(180, 40)
    world.add_worms(1000)
    world.add_trees(500)
    world.add_birds(50)
    # collect_data = threading.Thread(target=world.plot.update, args=(world,))
    # collect_data.start()

    keyboard_listener = threading.Thread(target=keyboard_controller, args=(world, window))
    keyboard_listener.start()

    while not world.sim_over:
        window.clear()
        window.insstr(0, 0, str(world))
        window.refresh()
        time.sleep(0.1)

        world.refresh()

    keyboard_listener.join()
    world.end()
    return


if __name__ == "__main__":
    curses.wrapper(run)
