import pandas as pd

class Player:

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
    def contribute(self, avg_prev_contributions=1, numOfRounds=10):
        # arguments: round t, prev contribution, average of previous round's contributions
        # set default value for avg_prev_contributions = 1 to avoid runtime error for initial contributions
        # return value cannot be less than 0 nor greater than 10
        if len(self.cont_hx) is 0:
            self.cont_hx.append(self.ic)
            return self.ic
        amount = self.b1 * self.cont_hx[-1] + self.b2 \
                * (1 - self.disc ** (numOfRounds - len(self.cont_hx) + 2)) \
                / (1- self.disc) * avg_prev_contributions
        self.cont_hx.append(amount)
        return amount

    # get contribution hx
    def get_hx(self):
        return self.cont_hx

class RosterIterator:
    """ Iterator class """
    def __init__(self, roster):
        self.r_list = roster._roster
        self._index = 0

    def __next__(self):
        """ Returns the next item from roster object's list """
        if self._index < (len(self.r_list)):
            result = self.r_list[self._index]
            self._index += 1
            return result
        # End of iteration
        raise StopIteration

class Roster:
    def __init__(self):
        self._roster = []

    def add_player(self, beta1, beta2, discount, initialOffering=5):
        self._roster.append(Player(beta1, beta2, discount, initialOffering))

    def __iter__(self):
        """Returns the Iterator object """
        return RosterIterator(self)


class PGG_Instance:
    # Number of rounds (default = 10)
    def __init__(self, roster_of_players, numOfRounds=10):
        self._roster_list = roster_of_players._roster
        self.totalRounds = numOfRounds
        self.currentRound = 0
        self.avg_contributions = []
        self.active_status = True

    def __repr__(self):
        return f'PGG_Instance({len(self._roster_list)!r} players, rounds: \
                {self.totalRounds!r}, current round: {self.currentRound!r}, \
                avg_contribs: {self.avg_contributions!r}, active: \
                {self.active_status!r})'

    def initialization(self):
        self.currentRound = 1
        contribs = []
        for i in self._roster_list:
            contribs.append(i.contribute())
        avg_contrib = sum(contribs) / len(self._roster_list)
        self.avg_contributions.append(avg_contrib)

    def next_round(self):
        if self.currentRound < self.totalRounds:
            self.currentRound += 1
            contribs = []
            for i in self._roster_list:
                contribs.append(i.contribute(self.avg_contributions[-1], \
                                            self.totalRounds))
            avg_contrib = sum(contribs) / len(self._roster_list)
            self.avg_contributions.append(avg_contrib)
        else:
            self.active_status = False

    # Snapshot: append data to csv file that maintains data generated for this run
    def create_instance_df(self):
        params={}
        contributions={}
        for i, player in enumerate(self._roster_list,1):
            params[f'p{i} beta1'] = [player.b1 for i in
                                        range(self.totalRounds)]
            params[f'p{i} beta2'] = [player.b2 for i in
                                        range(self.totalRounds)]
            params[f'p{i} discount'] = [player.disc for i in \
                                        range(self.totalRounds)]
            contributions[f'p{i} contributions'] = player.get_hx()
        dfp = pd.DataFrame(params, index=list(range(1,self.totalRounds+1)))
        dfc = pd.DataFrame(contributions, index=list(range(1,self.totalRounds+1)))
        df = pd.concat([dfp,dfc], axis=1)
        df['Round #'] = list(range(1,self.totalRounds+1))
        return df
