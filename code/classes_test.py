# classes_test.py
from unittest import TestCase, main
import classes
import numpy as np

class PlayerTestCase(TestCase):
    # def test_stoch_player(self):
    #     pl1 = classes.StochPlayer(0.4,0.5)
    #     amount = pl1.contribute()
    #     self.assertEqual(len(pl1.cont_hx), 1)
    #     if amount is 10.0:
    #         self.assertEqual(pl1.cont_hx[-1], 10.0)
    #     else:
    #         self.assertEqual(pl1.cont_hx[-1], 0)
    #
    # def test_player_contribute(self):
    #     pl1 = classes.TfPlayer(4,5)
    #     self.assertEqual(pl1.contribute(3), 5)

    def test_fj_player_(self):
        pl1 = classes.FjPlayer(1,0.2)
        self.assertEqual(pl1.ic, 1)
        self.assertEqual(pl1.a, 0.2)
        pl1.contribute(3)
        self.assertEqual(pl1.cont_hx[-1], 3)

class RosterTestCase(TestCase):
    def test_roster(self):
        r1 = classes.Roster()
        self.assertEqual(r1._roster, [])

    # This test only considers FJ model
    def test_add_player(self):
        ic, alpha = 1, 0.5
        cache = ic, alpha
        r2 = classes.Roster()
        r2.add_player(cache, 'FJ')
        r2.add_player(cache, 'FJ')
        r2.add_player(cache, 'FJ')
        self.assertEqual(len(r2._roster),3)
        self.assertEqual(r2.model_type,'FJ')
        self.assertEqual(len(r2.X_0),3)

class PGG_InstanceTestCase(TestCase):
    def test_pgg_instance(self):
        ic, alpha = 1, 0.5
        cache = ic, alpha
        r3 = classes.Roster()
        r3.add_player(cache, 'FJ')
        r3.add_player(cache, 'FJ')
        r3.add_player(cache, 'FJ')
        r3.add_player(cache, 'FJ')
        r3.add_player(cache, 'FJ')
        t1 = classes.PGG_Instance(r3)
        self.assertEqual(len(t1._roster_list),5)
        self.assertEqual(t1.type, 'FJ')
        self.assertEqual(t1.W.shape, (5,5))
        self.assertEqual(np.array_equal(np.diag(np.diag(t1.W)), t1.Ident_Lambda),True)

    def test_initialization(self):
        ic, alpha = 1, 0.5
        cache = ic, alpha
        r4 = classes.Roster()
        r4.add_player(cache, 'FJ')
        r4.add_player(cache, 'FJ')
        r4.add_player(cache, 'FJ')
        r4.add_player(cache, 'FJ')
        r4.add_player(cache, 'FJ')
        t2 = classes.PGG_Instance(r4)
        t2.initialization()
        self.assertEqual(t2.X_k.shape, (5,))


if __name__ == '__main__':
    main()
