import numpy as np

class IsingLattice:

    E_list = []
    M_list  = []

#    n_cycles = 1
#    E = np.sum(E_list)
#    E2 = np.sum(E2_list)
#    M = np.sum(M_list)
#    M2 = np.sum(M2_list)

    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.lattice = np.random.choice([-1,1], size=(n_rows, n_cols))

    #def energy(self):
        #L = np.sum( # Find energy of interactions with left neighbour
        #    np.multiply(np.roll(self.lattice, 1, 1), self.lattice))
        #R = np.sum(  # Find energy of interactions with right neighbour
        #    np.multiply(np.roll(self.lattice, 1, 0), self.lattice))
        #return - L - R  # add the energies together

    def energy(self):
        "Return the total energy of the current lattice configuration."
        N = self.n_cols * self.n_rows # Total number of spin states
        energy = 0.0
        for i in range(N):
            col = int(i % self.n_cols)
            row = int((i - col) / self.n_cols) # generate cols and rows with one for loop
            energy += self.lattice[row][col] * self.lattice[row][col - 1] # interactions with left
            energy += self.lattice[row][col] * self.lattice[row - 1][col] # interactions with up
        return -energy

    def magnetisation(self):
        "Return the total magnetisation of the current lattice configuration."
        magnetisation = np.sum(self.lattice)
        return magnetisation

    def montecarlostep(self, T):
        "Executes Monte Carlo in a Single Step, updates the self quantities"
        e_old = self.energy()
        random_i = np.random.choice(range(0, self.n_rows)) # choose a random row, column to flip
        random_j = np.random.choice(range(0, self.n_cols))
        self.lattice[random_i][random_j] *=  -1 # random spin flipped
        e_new = self.energy()
        if e_new > e_old:
            Del_E = e_new - e_old
            p = np.e ** (-Del_E / T) # Monte Carlo condition
            random_number = np.random.random() # choose a random number in the range [0,1)

            if random_number > p:
                self.lattice[random_i][random_j] =  -self.lattice[random_i][random_j]

        self.E_list.append(self.energy())
        self.M_list.append(self.magnetisation())

        return self.energy(), self.magnetisation()

    def statistics(self):
        "Return average values for various properties"

        C_Off = 2000 # cut off point
        return [np.mean(self.E_list[C_Off:]),
                np.std(self.E_list[C_Off:]) ,
                np.mean(self.M_list[C_Off:]),
                np.std(self.M_list[C_Off:])
                #,self.n_cycles-C_Off
                ]

    def statistics_capacity(self, C_Off):
        "Return average values for various properties"
        return [np.mean(self.E_list[C_Off:]),
#                np.std(self.E_list[C_Off:]) ,
                np.mean(self.M_list[C_Off:]),
#                np.std(self.M_list[C_Off:]),
                np.mean(np.array(self.E_list[C_Off:])**2),
                np.mean(np.array(self.M_list[C_Off:])**2)
                ]
