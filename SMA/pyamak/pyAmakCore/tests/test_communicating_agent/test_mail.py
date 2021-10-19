"""
test that Mail work as intended
"""
from unittest import TestCase, main

from pyAmakCore.classes.communicating_agent import Mail


class TestMail(TestCase):
    """
    Test class Mail
    """

    def test_mail(self) -> None:
        """
        Test mail init
        """
        mail = Mail(1, 5, None, 0)

        self.assertEqual(mail.get_id_sender(), 1)
        self.assertEqual(mail.get_id_receiver(), 5)
        self.assertEqual(mail.get_message(), None)
        self.assertEqual(mail.get_sending_date(), 0)

        mail = Mail(255, 0, "test", 12)
        self.assertEqual(mail.get_id_sender(), 255)
        self.assertEqual(mail.get_id_receiver(), 0)
        self.assertEqual(mail.get_message(), "test")
        self.assertEqual(mail.get_sending_date(), 12)

if __name__ == '__main__':
    main()
