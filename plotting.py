import numpy as np
import matplotlib.pyplot as plt


class Plot:
    def __init__(self):
        self.w = []
        self.t = []
        self.b = []
        self.time = 0

    def get_data(self, wo, w, t, b):
        with wo.lock_map:
            self.w.append(len(w))
            self.t.append(len(t))
            self.b.append(len(b))
            self.time += 1

    def toggle_show(self):
        fig, ax = plt.subplots()
        ax.plot(np.arange(self.time), self.w, label='Worms')
        ax.plot(np.arange(self.time), self.t, label='Trees')
        ax.plot(np.arange(self.time), self.b, label='Birds')
        ax.set(xlabel='Time', ylabel='Population',
               title='Population over time')
        ax.legend()
        ax.grid()
        plt.savefig('plot.png')
