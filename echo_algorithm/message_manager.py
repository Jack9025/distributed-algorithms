from datetime import datetime
from random import randint


def time() -> float:
    """Gets the current timestamp"""
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    return ts


class MessageManager:
    def __init__(self, delay_msg=False):
        self.processes = []
        self.messages = {}
        self.delay_msg = delay_msg
        self.initialised = False

    def initialise(self, processes):
        assert len(processes) >= 2
        assert not self.initialised

        self.processes = processes
        self.messages = {}
        for process in processes:
            self.messages[process.p_id] = []

        self.initialised = True

    def has_message(self, p_id: int) -> bool:
        """Checks if p has received a message"""
        assert (p_id in self.messages)
        return len([m for m in self.messages[p_id] if m.has_arrived()]) >= 1

    def fetch_message(self, p_id: int) -> int:
        """Fetches process ids of message sent to p"""
        assert (self.has_message(p_id))
        available_msg = [m for m in self.messages[p_id] if m.has_arrived()]
        msg = available_msg[randint(0, len(available_msg) - 1)]  # Select a random message
        self.messages[p_id].remove(msg)  # Delete message
        return msg.s_id

    def add_message(self, p_id: int, q_id: int):
        """Adds message from p_id to q_id"""
        self.messages[q_id].append(Message(p_id, self.delay_msg))


class Message:
    def __init__(self, s_id: int, delay: bool):
        self.s_id = s_id
        self.delay = time()
        if delay:
            # Random delay upto 2 seconds
            self.delay += randint(0, 2000) / 1000

    def has_arrived(self) -> bool:
        """Checks if message has arrived"""
        return self.delay - time() < 0