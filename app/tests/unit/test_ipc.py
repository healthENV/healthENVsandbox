import unittest
import sys
sys.path.append('../..')
from ipc import sumOwn
from fractions import Fraction


class TestSum(unittest.TestCase):
    """ Testing
    """
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = sumOwn(data)
        self.assertEqual(result, 6)

    def test_list_fraction(self):
        """
        Test that it can sum a list of fractions
        """
        data = [Fraction(1, 4), Fraction(1, 4), Fraction(2, 5)]
        result = sumOwn(data)
        self.assertEqual(result, 1)

    def test_bad_type(self):
        data = "banana"
        with self.assertRaises(TypeError):
            result = sumOwn(data)

if __name__ == '__main__':
    unittest.main()