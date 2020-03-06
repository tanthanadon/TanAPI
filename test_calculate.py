import unittest

from app import calculateDistance

class BasicTests(unittest.TestCase):

    def test_input(self):
        d = calculateDistance(14.977660, 102.083679, 14.353462, 100.569003)
        
        self.assertGreater(d, 0)
        

if __name__ == '__main__':
    unittest.main()