from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import random
import copy

# class Creator(ABC):
#     """
#     Creator class provides the factory method that should return different
#     Player models. The subclasses will provide the implementation for each
#     model.
#     """
#     @abstractmethod
#     def factory_method(self):
#         pass
#
# class TfCreator(Creator):
#     def factory_method(self) -> TfPlayer:
#         return TfPlayer()
#
# class DtfCreator(Creator):
#     def factory_method(self) -> DtfPlayer:
#         return DtfPlayer()
#
# class StochTfCreator(Creator):
#     def factory_method(self) -> StochTfPlayer:
#         return StochTfPlayer()
#
# class StochDtfCreator(Creator):
#     def factory_method(self) -> StochDtfPlayer:
#         return StochDtfPlayer()

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
    def contribute(self):
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

class SimpStochPlayer(Player):
    def __init__(self, eps, i_cont, alpha=0):
        self.eps = eps
        self.cont_hx = list()
        self.nghb_hx = list()
        self.e_hx = [1]
        self.ic = i_cont # random.randrange(0,2) * self.e_hx[-1]
        self.a = alpha

    def contribute(self, numOfRounds=10):
        if len(self.cont_hx) is 0:
            self.cont_hx.append(self.ic)
            return self.ic

        # Code block to handle the uniform option - where player contributes a uniform value
        if self.a != 0:
            uni_chance_roll = random.random()
            if uni_chance_roll < self.a:
                cont_amount = random.random()
                if cont_amount > self.e_hx[-1]:
                    cont_amount = self.e_hx[-1]
                self.cont_hx.append(cont_amount)
                return cont_amount

        chance_roll = random.random()
        x_n, y_n = self.nghb_hx[-1]  # x_n - fraction played 1;
                                     # y_n - fraction played 0
        ex = self.eps * x_n
        y = y_n

        if self.cont_hx[-1] == 0:  # S0 - case that previous contribution was 0
            if chance_roll < (1-ex) :
                cont_amount = 0
            else:
                cont_amount = 1
                if cont_amount > self.e_hx[-1]:
                    cont_amount = self.e_hx[-1]
        elif self.cont_hx[-1] == 1:  # S1 - case that previous contribution was 1
            if chance_roll < y:
                cont_amount = 0
            else:
                cont_amount = 1
                if cont_amount > self.e_hx[-1]:
                    cont_amount = self.e_hx[-1]
        else:
            cont_amount = 0
        self.cont_hx.append(cont_amount)
        return cont_amount

    def input_fractions(self, fractions_tuple):
        self.nghb_hx.append(fractions_tuple)

class FjPlayer(Player):
    def __init__(self, i_cont, alpha):
        self.cont_hx = list()
        # self.nghb_hx = list()
        self.e_hx = [1]
        self.ic = i_cont
        self.a = alpha

    def contribute(self, contribution):
        """
        Contribute function for FJ player just pushes contribution value to
        contribution history list.
        """
        self.cont_hx.append(contribution)

    # def input_fractions(self, fractions_tuple):
    #     self.nghb_hx.append(fractions_tuple)

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
        if type == 'TF':
            beta1, beta2 = cache
            self._roster.append(TfPlayer(beta1, beta2))
            if self.model_type == None:
                self.model_type = 'TF'
        elif type == 'STF':
            beta1, beta2, initial_contribution = cache
            self._roster.append(StochPlayer(beta1, beta2, initial_contribution))
            if self.model_type == None:
                self.model_type = 'STF'
        elif type == 'SST':
            eps, initial_contribution, alpha = cache
            self._roster.append(SimpStochPlayer(eps, initial_contribution,
                                                alpha))
            if self.model_type == None:
                self.model_type = 'SST'
        elif type == 'FJ':
            initial_state, alpha = cache  # initial state (aka initial contribution)
            self._roster.append(FjPlayer(initial_state, alpha))
            if self.model_type == None:
                self.model_type = 'FJ'
                self.X_0 = [initial_state]
            else:
                self.X_0.append(initial_state)
        elif type == 'FJ2':
            initial_state, alpha = cache  # initial state (aka initial contribution)
            self._roster.append(FjPlayer(initial_state, alpha))
            if self.model_type == None:
                self.model_type = 'FJ2'
                self.X_0 = [initial_state]
            else:
                self.X_0.append(initial_state)
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
        if self.type[:2] == 'FJ':
            # Initialize X_0
            self.X_0 = roster_of_players.X_0
            self.W = self.compute_W()
            self.Lambda = np.zeros((5,5))

            self.X_k = None
            self.X_k_and_1 = None
            # np.fill_diagonal(self.W, alpha)
            np.fill_diagonal(self.Lambda, 1-self.W.diagonal())
            self.Ident_Lambda = np.identity(5) - self.Lambda

        self.totalRounds = numOfRounds
        self.currentRound = 0
        self._m_factor = multiplicativeFactor
        self.active_status = True

    def compute_W(self):
        """
        Helper function to iterate through roster list and generate
        interpersonal weight matrix with individual players' alpha param.
        """
        preW = []
        num_elems = len(self._roster_list)
        for pos, i in enumerate(self._roster_list):
            alpha = i.a
            row = [(1-alpha)/(num_elems-1) for x in range(num_elems)]
            row[pos] = alpha
            preW.append(row)
        return np.array(preW)

    def __repr__(self):
        return f'PGG_Instance({len(self._roster_list)!r} players, rounds: \
                {self.totalRounds!r}, current round: {self.currentRound!r}, \
                avg_contribs: {self.avg_contributions!r}, active: \
                {self.active_status!r})'

    def initialization(self):
        self.currentRound = 1
        if self.type == 'SST':
            contribs = list(self.roster_contribs_iter())
            num_ones = contribs.count(1)
            num_zeros = contribs.count(0)
            fract_p_one = num_ones/5
            fract_p_zero = num_zeros/5
            fractions = (fract_p_one, fract_p_zero)
            self.submit_fractions(fractions)
            self.comp_payout(sum(contribs))
        elif self.type == 'FJ':
            self.X_k = np.array(copy.deepcopy(self.X_0))
            diff = np.array(self.roster_endowment_check()) - self.X_k
            diff[diff > 0] = 0
            self.X_k += diff

            self.roster_contribs_push(self.X_k)
            self.comp_payout(sum(self.X_k))
        elif self.type == 'FJ2':
            self.X_k = np.array(copy.deepcopy(self.X_0))
            outer_prod = np.outer(self.X_k,
                                    np.array(self.roster_endowment_check()))
            contributions = np.diagonal(outer_prod)
            # diff = np.array(self.roster_endowment_check()) - self.X_k
            # diff[diff > 0] = 0
            # self.X_k += diff

            self.roster_contribs_push(contributions)
            self.comp_payout(sum(contributions))
        else:
            contribs = list(self.roster_contribs_iter())
            self.compute_roster_neigh_avgs(sum(contribs))
            self.comp_payout(sum(contribs))

    def roster_contribs_iter(self):
        """Iterator that iterates roster list and generates player contribution"""
        for i in self._roster_list:
            yield i.contribute(self.totalRounds)

    def roster_contribs_push(self, contributions):
        """For-loop that iterates roster list and pushes contributions to each player """
        for num, player in enumerate(self._roster_list):
            cont = contributions[num]
            player.contribute(cont)

    def roster_endowment_check(self):
        """For-loop that iterates roster list and pulls endowments for each player """
        prev_e = []
        for num, player in enumerate(self._roster_list):
            prev_e.append(player.e_hx[-1])
        return prev_e

    def compute_roster_neigh_avgs(self, all_contribs):
        """For-loop that iterates roster list and computes neighbor avgs"""
        for i in self._roster_list:
            i.computeNeighborAvg(all_contribs,len(self._roster_list))

    def submit_fractions(self, fractions):
        """For-loop that iterates roster list and computes neighbor avgs"""
        for i in self._roster_list:
            i.input_fractions(fractions)

    def comp_payout(self, all_contribs):
        for i in self._roster_list:
            i.payout(all_contribs, self._m_factor, len(self._roster_list))

    def next_round(self):
        """Instance method to play a single round"""
        if self.currentRound < self.totalRounds:
            self.currentRound += 1
            if self.type == 'FJ':
                self.X_k_and_1 = np.matmul(np.matmul(self.Lambda, self.W), self.X_k) \
                            + np.matmul(self.Ident_Lambda, self.X_0)
                diff = self.roster_endowment_check() - self.X_k_and_1
                diff[diff > 0] = 0
                self.X_k_and_1 += diff

                self.roster_contribs_push(self.X_k_and_1)
                totl_contribs = sum(self.X_k_and_1)
                self.X_k = self.X_k_and_1
            elif self.type == 'FJ2':
                self.X_k_and_1 = np.matmul(np.matmul(self.Lambda, self.W), self.X_k) \
                            + np.matmul(self.Ident_Lambda, self.X_0)
                outer_prod = np.outer(self.X_k_and_1,
                                        np.array(self.roster_endowment_check()))
                contributions = np.diagonal(outer_prod)

                self.roster_contribs_push(contributions)
                totl_contribs = sum(contributions)
                self.X_k = self.X_k_and_1
            else:
                contribs = list(self.roster_contribs_iter())
                totl_contribs = sum(contribs)
                if self.type == 'SST':
                    num_ones = contribs.count(1)
                    num_zeros = contribs.count(0)
                    fract_p_one = num_ones/5
                    fract_p_zero = num_zeros/5
                    fractions = (fract_p_one, fract_p_zero)
                    self.submit_fractions(fractions)
                else:
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
            if self.type == 'SST':
                params[f'p{i} Epsilon'] = [player.eps for i in
                                            range(self.totalRounds)]
                params[f'p{i} Alpha'] = [player.a for i in
                                            range(self.totalRounds)]
            elif self.type[:2] == 'FJ':
                params[f'p{i} Alpha'] = [player.a for i in
                                            range(self.totalRounds)]
            else:
                params[f'p{i}_b1'] = [player.b1 for i in
                                        range(self.totalRounds)]
                params[f'p{i}_b2'] = [player.b2 for i in
                                        range(self.totalRounds)]
            if self.type == 'DTF':
                params[f'p{i}_disc'] = [player.disc for i in \
                                            range(self.totalRounds)]
            contributions[f'p{i}_cont'] = player.cont_hx
            contributions[f'new_p{i}_e'] = player.e_hx[1:]
        dfp = pd.DataFrame(params, index=list(range(1,self.totalRounds+1)))
        dfc = pd.DataFrame(contributions, index=list(range(1,self.totalRounds+1)))
        df = pd.concat([dfp,dfc], axis=1)
        df['Round'] = list(range(1,self.totalRounds+1))
        return df
