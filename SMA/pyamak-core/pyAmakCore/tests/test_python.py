"""
Tests that python actually runs
"""

from unittest import TestCase, main


class TestPython(TestCase):
    """
    Tests that python runs
    """
    def test_one_equals_one(self) -> None:
        """
        Tests a true assumption
        """
        self.assertEqual(1, 1)


if __name__ == '__main__':
    main()
