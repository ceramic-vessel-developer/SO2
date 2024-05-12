import numpy as np
import matplotlib.pyplot as plt
import time


class Plot:
    def __init__(self):
        self.w = []
        self.t = []
        self.b = []
        self.time = 0

    def get_data(self, wo):
        time.sleep(0.15)
        with wo.lock_map:
            self.w.append(len(wo.worms))
            self.t.append(len(wo.trees))
            self.b.append(len(wo.birds))
            self.time += 1

    def update(self, wo):
        self.get_data(wo)
        x = np.arange(self.time)
        fig, ax = plt.subplots()
        ax.plot(x, self.w, label='Worms')
        ax.plot(x, self.t, label='Trees')
        ax.plot(x, self.b, label='Birds')
        ax.set(xlabel='Time', ylabel='Population',
               title='Population over time')
        ax.legend()
        ax.grid()

    def toggle_show(self):
        plt.show()
