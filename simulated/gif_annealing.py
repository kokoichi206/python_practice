import numpy as np
from abc import *
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image


class StatModel (ABC):

    def __init__ (self, N, J, h):
        self.N = N
        self.J = J
        self.h = h

    @abstractmethod
    def hamiltonian (self, state):
        raise NotImplementedError()

    @abstractmethod
    def update (self, state):
        raise NotImplementedError()

    @abstractmethod
    def initializeState(self):
        raise NotImplementedError()

    def prob (self, current, proposal, temperature):
        tmp = np.exp ((current-proposal)/temperature)
        return min ([tmp,1.])

    def scheduleLogarithm (self, step, beta0=1.0):
        return 1/ (beta0 * np.log (2+step))


    def annealing (self, maxStep, Tinit=1e3, C=0.995, seed=24):
        '''
        雑にSAする
        '''
        np.random.seed(seed)
        t = Tinit
        hams = []
        ts = []
        state = self.initializeState()
        startTime = time.time()
        times = []
        
        # to save all state
        states = []

        for step in range(maxStep):
            ham = self.hamiltonian(state)
            hams.append(ham)
            states.append(state)
            times.append(time.time()-startTime)
            proposal = self.update(state.copy ())
            hamprop = self.hamiltonian(proposal)
            if (np.random.rand() < self.prob(ham,hamprop,t)):
                state = proposal

            t *= C    # 温度を下げる
            


        hams.append(ham)
        times.append(time.time()-startTime)
        return states, hams, times


class IsingModel(StatModel):

    def __init__(self, N, J, h):
        super().__init__(N, J, h.reshape((N,)))


    # override
    def hamiltonian(self, state):
        tmp1 = -0.5 * state.reshape((1,self.N)) @ self.J @ state.reshape((self.N,1))
        tmp2 = -state.reshape((1,self.N)) @ self.h
        return (tmp1 + tmp2)[0,0]

    # override
    def update(self, state):
        idx = np.random.randint(low=0,high=self.N)
        state[idx] = - state[idx]    # flip
        return state

    # override
    def initializeState(self):
        return np.sign(np.random.randn(self.N,))

def dipict_ims_for_gif(states, enes, times, maxStepi, step_i, bond_interaction):
    # make figure part
    finish_time = times[-1]
    max_energy = max(enes)
    min_energy = min(enes)
    times_normalized = [x / finish_time for x in times]
    enes_normalized = [(y - min_energy) / (max_energy - min_energy) for y in enes]

    # step_i = 50 # how often do u wanna record?

    if bond_interaction > 0:
        bon = 'FM'
    elif bond_interaction < 0:
        bon = 'AFM'

    ims = []
    for j in range(maxStepi // step_i):
        i = j * step_i
        print('i = ',i)
        fig, axes = plt.subplots(nrows=1, ncols=2, sharex=False, figsize=(16,8))
        # figs = plt.figure() # is needed?
        # plt.plot(times, enes)
        fig.canvas.draw()

        # write the title
        plt.tight_layout()
        fig.suptitle(f'{bon} Ising Nearest', fontsize=20)
        plt.subplots_adjust(top=0.9)

        plt.rcParams["font.family"] = "Arial"      #全体のフォントを設定
        plt.rcParams["xtick.direction"] = "in"               #x軸の目盛線を内向きへ
        plt.rcParams["ytick.direction"] = "in"               #y軸の目盛線を内向きへ
        plt.rcParams["xtick.minor.visible"] = False        #x軸補助目盛りの追加
        plt.rcParams["ytick.minor.visible"] = True           #y軸補助目盛りの追加
        plt.rcParams["xtick.major.width"] = 1.5              #x軸主目盛り線の線幅
        plt.rcParams["ytick.major.width"] = 1.5              #y軸主目盛り線の線幅
        plt.rcParams["xtick.minor.width"] = 1.0              #x軸補助目盛り線の線幅
        plt.rcParams["ytick.minor.width"] = 1.0              #y軸補助目盛り線の線幅
        plt.rcParams["xtick.major.size"] = 10                #x軸主目盛り線の長さ
        plt.rcParams["ytick.major.size"] = 10                #y軸主目盛り線の長さ
        plt.rcParams["xtick.minor.size"] = 5                 #x軸補助目盛り線の長さ
        plt.rcParams["ytick.minor.size"] = 5                 #y軸補助目盛り線の長さ
        plt.rcParams["font.size"] = 14                       #フォントの大きさ
        plt.rcParams["axes.linewidth"] = 1.5                 #囲みの太さ

        # axes[0].imshow(states[i].reshape(li,li), cmap="seismic")
        axes[0].imshow(states[i].reshape(li,li))

        axes[1].set_xlim(0,1.05)
        axes[1].set_ylim(-0.05,1.05)
        axes[1].plot(times_normalized[0:i+1], enes_normalized[0:i+1])
        axes[1].set_xlabel(f'step_num ({maxStepi})', fontsize=15)
        axes[1].set_ylabel('energy', fontsize=15)
        # ene_min = -523776 is 0
        axes[1].set_yticks([0.044, 0.52, 1])
        yticklabels = ([-50, -25, 0])
        axes[1].set_yticklabels(yticklabels)
        axes[1].set_xticks([0, 1])
        xticklabels = ([0, maxStepi])
        axes[1].set_xticklabels(xticklabels)
        # add circle at the end of the graph
        c = patches.Circle(xy=(times_normalized[i], enes_normalized[i]), radius=0.01, fc='g', ec='r')
        axes[1].add_patch(c)

        fig.savefig('Ising.png')
        # convert Image object
        image_array = np.array(fig.canvas.renderer.buffer_rgba())
        im = Image.fromarray(image_array)
        ims.append(im)
        plt.close(fig)

    return ims

# To find nearest bonds for each cite
def nearest_bond(l, interaction=1.0):
    # to treat each cite with one integer
    N = l * l
    # l is the length of one side
    Ji = np.zeros((N, N))
    for i in range(N):
        x = i % l
        y = i // l
        if x == 0:
            Ji[i][i+1] = interaction
        elif x == l - 1:
            Ji[i][i-1] = interaction
        else:
            Ji[i][i-1] = interaction
            Ji[i][i+1] = interaction
        if y == 0:
            Ji[i][i+l] = interaction
        elif y == l - 1:
            Ji[i][i-l] = interaction
        else:
            Ji[i][i-l] = interaction
            Ji[i][i+l] = interaction

    if interaction > 0:
        bond = 'FM'
    elif interaction < 0:
        bond = 'AFM'
    return Ji, bond


li = 32
Ni = li*li

# the definition of Hamiltonian
# infinite-range model
# Ji = np.ones((Ni,Ni)) - np.eye(Ni)
# nearest neighbor model

bond_interaction = -1.0
Ji, bond = nearest_bond(li,bond_interaction)

hi = np.zeros((Ni,1))
maxStepi = 10000
# maxStepi = 20000
step_i = 30

modeli = IsingModel(Ni,Ji,hi)
states, enes, times = modeli.annealing (maxStepi)

# print(enes)

# print(min_energy)



ims = dipict_ims_for_gif(states, enes, times, maxStepi, step_i, bond_interaction)
ims[0].save(f'./gif/{bond}_Ising_{maxStepi}step_.gif', save_all=True, append_images=ims[1:], loop=0, duration=50)