class Player:

    # Class Attribute
    # prev_avg_conts = list()

    # Initializer / Instance Attributes
    def __init__(self, beta1, beta2, discount, initialCont=5):
        self.b1 = beta1
        self.b2 = beta2
        self.disc = discount
        self.ic = initialCont
        self.cont_hx = list()
    def __repr__(self):
        return f'Player({self.b1!r}, {self.b2!r}, {self.disc!r}, {self.ic!r},\
                        {self.cont_hx!r})'
    # Contribute (and add value to contribution hx) --> int
    def contribute(self, numOfRounds):
        # arguments: round t, prev contribution, average of previous round's contributions
        # return value cannot be less than 0 nor greater than 10
        if len(self.cont_hx) is 0:
            self.cont_hx.append(self.ic)
            return self.ic
        amount = self.b1 * self.cont_hx[-1] + self.b2 \
                * (1 - self.disc ** (numOfRounds - len(self.cont_hx) + 2)) \
                / (1-discount) * avg_prev_contributions
        self.cont_hx.append(amount)
        return amount

    # get contribution hx
    def get_hx(self):
        return self.cont_hx

class Round:
    # each player contributes
    # compute average of avg of contributions
    pass

class PGG_Instance:
    # Number of rounds (default = 10)
    # Number of players (default = 5)
    # List of average contributions for each round?
    # Snapshot: append data to csv file that maintains data generated for this run
    pass
