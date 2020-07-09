from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd
import random

class Creator(ABC):
    """
    Creator class provides the factory method that should return different
    Player models. The subclasses will provide the implementation for each
    model.
    """
    @abstractmethod
    def factory_method(self):
        pass

class TfCreator(Creator):
    def factory_method(self) -> TfPlayer:
        return TfPlayer()

class DtfCreator(Creator):
    def factory_method(self) -> DtfPlayer:
        return DtfPlayer()

class StochTfCreator(Creator):
    def factory_method(self) -> StochTfPlayer:
        return StochTfPlayer()

class StochDtfCreator(Creator):
    def factory_method(self) -> StochDtfPlayer:
        return StochDtfPlayer()

class Player(ABC):
    """
    The Player interface declares the operations that all concrete players must
    implement.
    """
    def __init__(self, beta1, beta2, discount):
        self.b1 = beta1
        self.b2 = beta2
        self.disc = discount
        self.cont_hx = list()
        self.nghb_avg_hx = list()
        self.e_hx = [10]
        self.ic = beta1 * self.e_hx[-1]


    def __repr__(self):
        return f'Player({self.b1!r}, {self.b2!r}, {self.disc!r}, \
                        {self.cont_hx!r})'

    @abstractmethod
    def contribute(self, numOfRounds=10):
        # arguments: round t, prev contribution, average of previous round's contributions
        # set default value for avg_prev_contributions = 1 to avoid runtime error for initial contributions
        # return value cannot be less than 0 nor greater than 10
        pass

    def computeNeighborAvg(self, totl_round_contribs, rosterSize=5):
        totalNeighContribs = totl_round_contribs - self.cont_hx[-1]
        neighAvg = totalNeighContribs/(rosterSize-1)
        self.nghb_avg_hx.append(neighAvg)

    def payout(self, totl_round_contribs, mfactor, num_of_players):
        payout_amnt = self.e_hx[-1] - self.cont_hx[-1] + (mfactor \
                        * (totl_round_contribs)) / num_of_players # TB Continued....
        self.e_hx.append(payout_amnt)

class TfPlayer(Player):
    def __init__(self, beta1, beta2):
        self.b1 = beta1
        self.b2 = beta2
        self.cont_hx = list()
        self.nghb_avg_hx = list()
        self.e_hx = [10]
        self.ic = beta1 * self.e_hx[-1]

    def contribute(self, avg_prev_contributions=1, numOfRounds=10):
        # arguments: round t, prev contribution, average of previous round's contributions
        # set default value for avg_prev_contributions = 1 to avoid runtime error for initial contributions
        # return value cannot be less than 0 nor greater than 10
        if len(self.cont_hx) is 0:
            if self.ic > 10:
                self.cont_hx.append(10)
                return 10
            self.cont_hx.append(self.ic)
            return self.ic
        amount = self.b1 * self.cont_hx[-1] + self.b2 * self.nghb_avg_hx[-1]
        # Threshold contribution amount when amount > endowment
        if amount > self.e_hx[-1]:
            amount = self.e_hx[-1]
        self.cont_hx.append(amount)
        return amount

class DtfPlayer(Player):
    # Contribute (and add value to contribution hx) --> int
    def contribute(self, avg_prev_contributions=1, numOfRounds=10):
        # arguments: round t, prev contribution, average of previous round's contributions
        # set default value for avg_prev_contributions = 1 to avoid runtime error for initial contributions
        # return value cannot be less than 0 nor greater than 10
        if len(self.cont_hx) is 0:
            if self.ic > 10:
                self.cont_hx.append(10)
                return 10
            self.cont_hx.append(self.ic)
            return self.ic
        amount = self.b1 * self.cont_hx[-1] + self.b2 \
                * (1 - self.disc ** (numOfRounds - len(self.cont_hx) + 2)) \
                / (1- self.disc) * self.nghb_avg_hx[-1]
        # Threshold contribution amount when amount > endowment
        if amount > self.e_hx[-1]:
            amount = self.e_hx[-1]
        self.cont_hx.append(amount)
        return amount

class StochPlayer(Player):
    def __init__(self, beta1, beta2, i_cont):
        self.b1 = beta1
        self.b2 = beta2
        self.cont_hx = list()
        self.nghb_avg_hx = list()
        self.e_hx = [10]
        self.ic = i_cont # random.randrange(0,2) * self.e_hx[-1]

    def contribute(self, avg_prev_contributions=1, numOfRounds=10):
        if len(self.cont_hx) is 0:
            self.cont_hx.append(self.ic)
            return self.ic
        chance_roll = random.random()

        if chance_roll < self.b1:
            if self.cont_hx[-1] <= self.e_hx[-1]:
                cont_amount = self.cont_hx[-1]
            else:
                cont_amount = self.e_hx[-1]

        elif self.b1 <= chance_roll < (self.b1 + self.b2):
            if self.nghb_avg_hx[-1] <= self.e_hx[-1]:
                cont_amount = self.nghb_avg_hx[-1]
            else:
                cont_amount = self.e_hx[-1]

        else:  # Changed model to introduce a 3rd probability -
               # where contribution amount is uniform RV (0,10)
            unif_rv_val = random.random() * 10
            if unif_rv_val <= self.e_hx[-1]:
                cont_amount = unif_rv_val
            else:
                cont_amount = self.e_hx[-1]

        self.cont_hx.append(cont_amount)
        return cont_amount

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
        self.model_type = None
    def add_player(self, cache, type='TF'):
        if type is 'TF':
            beta1, beta2 = cache
            self._roster.append(TfPlayer(beta1, beta2))
            self.model_type = 'TF'
        elif type is 'STF':
            beta1, beta2, initial_contribution = cache
            self._roster.append(StochPlayer(beta1, beta2, initial_contribution))
            self.model_type = 'STF'
        else:
            beta1, beta2, discount = cache
            self._roster.append(DtfPlayer(beta1, beta2, discount))
            self.model_type = 'DTF'

    def __iter__(self):
        """Returns the Iterator object """
        return RosterIterator(self)


class PGG_Instance:
    # Number of rounds (default = 10)
    def __init__(self, roster_of_players, numOfRounds=10, \
                multiplicativeFactor=1.2):
        self._roster_list = roster_of_players._roster
        self.type = roster_of_players.model_type
        self.totalRounds = numOfRounds
        self.currentRound = 0
        self._m_factor = multiplicativeFactor
        self.active_status = True

    def __repr__(self):
        return f'PGG_Instance({len(self._roster_list)!r} players, rounds: \
                {self.totalRounds!r}, current round: {self.currentRound!r}, \
                avg_contribs: {self.avg_contributions!r}, active: \
                {self.active_status!r})'

    def initialization(self):
        self.currentRound = 1
        contribs = []
        contribs = list(self.roster_contribs_iter())
        self.compute_roster_neigh_avgs(sum(contribs))
        self.comp_payout(sum(contribs))

    def roster_contribs_iter(self):
        """Iterator that iterates roster list and generates player contribution"""
        for i in self._roster_list:
            yield i.contribute(self.totalRounds)

    def compute_roster_neigh_avgs(self, all_contribs):
        """For-loop that iterates roster list and computes neighbor avgs"""
        for i in self._roster_list:
            i.computeNeighborAvg(all_contribs,len(self._roster_list))

    def comp_payout(self, all_contribs):
        for i in self._roster_list:
            i.payout(all_contribs, self._m_factor, len(self._roster_list))

    def next_round(self):
        """Instance method to play a single round"""
        if self.currentRound < self.totalRounds:
            self.currentRound += 1
            contribs = list(self.roster_contribs_iter())
            totl_contribs = sum(contribs)
            self.compute_roster_neigh_avgs(totl_contribs)
            self.comp_payout(totl_contribs)
        else:
            self.active_status = False

    # Snapshot: append data to csv file that maintains data generated for this run
    def create_instance_df(self):
        params={}
        contributions={}
        payoff={}
        for i, player in enumerate(self._roster_list,1):
            params[f'p{i} beta1'] = [player.b1 for i in
                                        range(self.totalRounds)]
            params[f'p{i} beta2'] = [player.b2 for i in
                                        range(self.totalRounds)]
            if self.type is 'DTF':
                params[f'p{i} discount'] = [player.disc for i in \
                                            range(self.totalRounds)]
            contributions[f'p{i} contributions'] = player.cont_hx
            contributions[f'p{i} e after round'] = player.e_hx[1:]
        dfp = pd.DataFrame(params, index=list(range(1,self.totalRounds+1)))
        dfc = pd.DataFrame(contributions, index=list(range(1,self.totalRounds+1)))
        df = pd.concat([dfp,dfc], axis=1)
        df['Round #'] = list(range(1,self.totalRounds+1))
        return df
