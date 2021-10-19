"""
test that Mailbox work as intended
"""
from unittest import TestCase, main

from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.communicating_agent import Mailbox
from pyAmakCore.classes.environment import Environment


class SimpleMailbox(Mailbox):

    def get_amas(self):
        return self._Mailbox__amas

    def get_owner_id(self):
        return self._Mailbox__owner_id

    def get_mail_list(self):
        return self._Mailbox__mail_list


class TestMailbox(TestCase):
    """
    Test class Mailbox
    """

    def test_init_mailbox(self) -> None:
        """
        Test mailbox init
        """

        environment = Environment()
        amas = Amas(environment)

        mailbox = SimpleMailbox(0, amas)

        self.assertEqual(mailbox.get_amas(), amas)
        self.assertEqual(mailbox.get_owner_id(), 0)
        self.assertEqual(mailbox.get_mail_list(), [])
        self.assertEqual(mailbox.get_mail(), None)


if __name__ == '__main__':
    main()
