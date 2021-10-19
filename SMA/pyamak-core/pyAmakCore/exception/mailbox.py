"""
exception for mailbox
"""


class ReceiverIsNotSelf(Exception):
    """
    this exception is called whenever you received a mail that is not sent to you
    """

    def __init__(self, self_id, message_id):
        self.self_id = self_id
        self.message_id = message_id
        super().__init__("Mail id is not self id")

    def __str__(self):
        return f' [Mailbox] : Mail id is not self id -> {self.message_id} != {self.self_id}'


class ReceiverDontExist(Exception):
    """
    this exception is called whenever you try to send a mail to someone that doesn't exist
    """

    def __init__(self, receiver_id):
        self.receiver_id = receiver_id
        super().__init__("receiver_id doesn't exist")

    def __str__(self):
        return f' [Mailbox] : Receiver_id could not be found -> {self.receiver_id}'
