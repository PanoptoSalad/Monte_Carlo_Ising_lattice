import numpy as np

class IsingLattice:

    E_list = []
    M_list  = []

    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.lattice = np.random.choice(np.arange(0,2*np.pi,0.001), size=(n_rows, n_cols)) # gives a lattice of random angles

    def energy(self):
        L = np.cos(np.roll(self.lattice, 1, 1)- self.lattice)
        R = np.cos(np.roll(self.lattice, 1, 0)- self.lattice)
        return np.sum(-L-R)

    def magnetisation(self):
        "Return the magnetisation magnitude of the current lattice configuration."
        x = np.sum(np.cos(self.lattice))
        y = np.sum(np.sin(self.lattice))
        complex1 = complex(x,y)
        return [np.absolute(complex1),np.angle(complex1)]

    def montecarlostep(self, T):
        "Executes Monte Carlo in a Single Step, updates the self quantities"
        e_old = self.energy()
        shape = np.copy(self.lattice)
        random_i = np.random.choice(range(0, self.n_rows)) # choose a random row, column to flip
        random_j = np.random.choice(range(0, self.n_cols))
        lattice_old = self.lattice[random_i][random_j]

        self.lattice[random_i][random_j] +=  np.random.random() * 2 * np.pi # random spin flipped
        if self.lattice[random_i][random_j] > 2 * np.pi:
            self.lattice[random_i][random_j] -= 2 * np.pi
        e_new = self.energy()
        if e_new > e_old:
            Del_E = e_new - e_old
            p = np.e ** (-Del_E / T) # Monte Carlo condition
            random_number = np.random.random() # choose a random number in the range [0,1)

            if random_number > p:
                self.lattice[random_i][random_j] = lattice_old

        eng = self.energy()
        mag = self.magnetisation()
        return [eng,mag,shape]

        return


    def statistics_capacity(self, C_Off):
        "Return average values for various properties"
        return [np.mean(self.E_list[C_Off:]),
                np.std(self.E_list[C_Off:]) ,
                np.mean(self.M_list[C_Off:]),
                np.std(self.M_list[C_Off:]),
                np.mean(np.array(self.E_list[C_Off:])**2),
                np.mean(np.array(self.M_list[C_Off:])**2)
                ]
