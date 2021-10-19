"""
test that nbr cycle of Amas work as intended
"""

from unittest import TestCase, main

from pytest import mark

from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.environment import Environment

class SimplerAmas(Amas):

    def synchronization(self):
        self._Amas__scheduler.give_amas_token()
        super().synchronization()



class TestAmasNbrCycle(TestCase):
    """
    Test class for Amas nbr cycle
    """

    @mark.timeout(10)
    def test_init_nbr_cycle(self) -> None:
        """
        test that nbr cycle init properly and add 1 to first cycle
        """
        environment = Environment()
        amas = SimplerAmas(environment)

        self.assertEqual(amas.get_cycle(), 0)

        amas.cycle()
        self.assertEqual(amas.get_cycle(), 1)

    @mark.timeout(20)
    def test_nbr_cycle_advanced(self) -> None:
        """
        test that nbr cycle add 1 each cycle
        """
        environment = Environment()
        amas = SimplerAmas(environment)
        for i in range(0, 10):
            with self.subTest(i=i):
                self.assertEqual(amas.get_cycle(), i)
            amas.cycle()


if __name__ == '__main__':
    main()
