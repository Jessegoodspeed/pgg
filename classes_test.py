# classes_test.py
from unittest import TestCase, main
from classes import Player

class PlayerTestCase(TestCase):
    def test_player_init(self):
        pl1 = Player(1,2,3)
        pl2 = Player(3,2,1)
        self.assertEqual(pl1.b2, pl2.b2)

    def test_player_contribute(self):
        pl1 = Player(4,5,6)
        self.assertEqual(pl1.contribute(3), 5)

    def test_player_get_hx(self):
        pl1 = Player(7,8,9)
        pl1.contribute(4)
        self.assertEqual(len(pl1.get_hx()),1)
        self.assertEqual(pl1.get_hx()[0],5)

if __name__ == '__main__':
    main()
