"""
Tests that python actually runs
"""

import unittest


class TestPython(unittest.TestCase):
    """
    Tests that python runs
    """
    def test_one_equals_one(self):
        """
        Tests a true assumption
        """
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
