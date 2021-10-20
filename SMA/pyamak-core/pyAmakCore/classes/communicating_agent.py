"""
Class Mail Mailbox and CommunicatingAgent
"""
from typing import Any, List
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.exception.mailbox import ReceiverIsNotSelf, ReceiverDontExist
from pyAmakCore.classes.agent import Agent


class Mail:
    """
    Class message
    """

    def __init__(self, id_sender: int, id_receiver: int, message: Any, sending_date: int) -> None:
        self.__id_sender: int = id_sender
        self.__id_receiver: int = id_receiver
        self.__message: Any = message
        self.__sending_date: int = sending_date

    def get_id_sender(self) -> int:
        """
        return sender id
        """
        return self.__id_sender

    def get_id_receiver(self) -> int:
        """
        return receiver id
        """
        return self.__id_receiver

    def get_message(self) -> Any:
        """
        return message
        """
        return self.__message

    def get_sending_date(self) -> int:
        """
        return sending_date
        """
        return self.__sending_date


class Mailbox:
    """
    Each agent have 1 unique mailbox that they can call to send or receive mail
    """

    def __init__(self, owner_id: int, amas: 'Amas') -> None:
        self.__mail_list: List['Mail'] = []
        self.__owner_id: int = owner_id
        self.__amas: 'Amas' = amas

    def get_mail(self) -> 'Mail':
        """
        return the next mail in the box, None if the mailBox is empty
        """
        if len(self.__mail_list) == 0:
            return None
        mail = self.__mail_list.pop()
        if mail.get_id_receiver() != self.__owner_id:
            raise ReceiverIsNotSelf(self.__owner_id, mail.get_id_receiver())
        return mail

    def receive_mail(self, mail: 'Mail'):
        """
        this method is called to put a mail in this mailbox
        """
        self.__mail_list.append(mail)

    def send_message(self, message: Any, id_receiver: int) -> None:
        """
        this method is called to send a message
        """
        mail = Mail(self.__owner_id, id_receiver, message, self.__amas.get_cycle())

        for agent in self.__amas.get_agents():
            if agent.get_id() == id_receiver:
                return agent.receive_mail(mail)
        raise ReceiverDontExist(id_receiver)


class CommunicatingAgent(Agent):
    """
    Agent class that can communicate
    """

    def __init__(self, amas: 'Amas') -> None:
        super().__init__(amas)
        self.__mailbox: 'Mailbox' = Mailbox(self.get_id(), amas)

    def send_message(self, message: Any, id_receiver: int) -> None:
        """
        send a message to another agent
        """
        self.__mailbox.send_message(message, id_receiver)

    def receive_mail(self, mail: 'Mail') -> None:
        """
        this method is called by another mailbox to add a mail in the mailbox
        """
        self.__mailbox.receive_mail(mail)

    def read_mails(self) -> None:
        """
        method that open all mail in the mailbox
        """
        mail = self.__mailbox.get_mail()
        while mail is not None:
            self.read_mail(mail)
            mail = self.__mailbox.get_mail()

    def read_mail(self, mail: 'Mail') -> None:
        """
        This method should be override to make an action whenever you read a mail
        """
