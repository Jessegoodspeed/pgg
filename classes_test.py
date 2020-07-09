# classes_test.py
from unittest import TestCase, main
import classes

class PlayerTestCase(TestCase):
    def test_stoch_player(self):
        pl1 = classes.StochPlayer(0.4,0.5)
        amount = pl1.contribute()
        self.assertEqual(len(pl1.cont_hx), 1)
        if amount is 10.0:
            self.assertEqual(pl1.cont_hx[-1], 10.0)
        else:
            self.assertEqual(pl1.cont_hx[-1], 0)

    def test_player_contribute(self):
        pl1 = classes.TfPlayer(4,5)
        self.assertEqual(pl1.contribute(3), 5)


if __name__ == '__main__':
    main()
