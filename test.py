from main import Enemy
import consts

import unittest

class EnemyTests(unittest.TestCase):
    
    def CoordinateInitiationSparx(self):
        """ If the initial coordinate are in the correct range for Sparx. """
        for i in range(0,100):
            x, y =  Enemy._Sparx().get_coordinate()

            if x in [consts.MARGIN, consts.MAP_DIM - consts.MARGIN]:
                self.assertTrue(y >= consts.MARGIN & y <= consts.MAP_HEIGHT - consts.MARGIN)
            else:
                self.assertTrue(x >= consts.MARGIN & x <= consts.MAP_DIM - consts.MARGIN)

if __name__ == '__main__':
    unittest.main(exit=True)