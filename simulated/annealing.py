import numpy as np
from abc import *
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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

li = 32
Ni = li*li
Ji = np.ones((Ni,Ni)) - np.eye(Ni)
hi = np.zeros((Ni,1))
# maxStepi = 10000
maxStepi = 100

modeli = IsingModel(Ni,Ji,hi)
states, enes, times = modeli.annealing (maxStepi)


# make figure part
finish_time = times[-1]
max_energy = max(enes)
times_normalized = [x / finish_time for x in times]
enes_normalized = [y / max_energy for y in enes]

fig, axes = plt.subplots(nrows=1, ncols=2, sharex=False, figsize=(16,8))
plt.figure()
# plt.plot(times, enes)

axes[0].imshow(states[-1].reshape(li,li))

i = 50
axes[1].set_xlim(0,1.1)
axes[1].set_ylim(0,1.1)
axes[1].plot(times_normalized[0:i+1], enes_normalized[0:i+1])
axes[1].set_xlabel('time', fontsize=15)
axes[1].set_ylabel('energy', fontsize=15)

# add circle at the end of the graph
c = patches.Circle(xy=(times_normalized[i], enes_normalized[i]), radius=0.01, fc='g', ec='r')
axes[1].add_patch(c)

# plt.xlabel('time[sec]')
# plt.ylabel('energy')
# plt.figure()
# plt.imshow(statei.reshape (li,li))
# plt.show()
fig.savefig('Ising.png')