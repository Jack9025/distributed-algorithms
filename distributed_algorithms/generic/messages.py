from datetime import datetime
from random import randint


def time() -> float:
    """Gets the current timestamp"""
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    return ts


class Message:
    def __init__(self, s_id: int):
        self.s_id = s_id
        self.delay = time()

    def add_delay(self):
        """Adds random delay of upto 2 seconds to message delivery time"""
        self.delay += randint(0, 2000) / 1000

    def has_arrived(self) -> bool:
        """Checks if message has arrived"""
        return self.delay - time() < 0


class MessageManager:
    def __init__(self, delay_msg=False):
        self.processes = []
        self.messages = {}
        self.logs = []
        self.delay_msg = delay_msg
        self.message_count = 0
        self.initialised = False

    def initialise(self, processes):
        assert len(processes) >= 2
        assert not self.initialised

        self.processes = processes
        self.messages = {}
        for process in processes:
            self.messages[process.p_id] = []

        self.message_count = 0
        self.initialised = True

    def has_message(self, p_id: int, msg_class=None) -> bool:
        """Checks if p has received a message"""
        assert (p_id in self.messages)
        return len([m for m in self.messages[p_id] if m.has_arrived() and
                    (msg_class is None or type(m) == msg_class)]) >= 1

    def fetch_message(self, p_id: int, msg_class=None) -> Message:
        """Fetches process ids of message sent to p"""
        assert self.has_message(p_id, msg_class)
        available_msg = [m for m in self.messages[p_id] if m.has_arrived() and
                         (msg_class is None or type(m) == msg_class)]
        msg = available_msg[randint(0, len(available_msg) - 1)]  # Select a random message
        self.messages[p_id].remove(msg)  # Delete message
        return msg

    def add_message(self, q_id: int, msg: Message):
        """Adds message sent to q"""
        if self.delay_msg:
            msg.add_delay()
        self.messages[q_id].append(msg)
        self.message_count += 1

    def log(self, msg: str):
        """Adds message to logs"""
        self.logs.append(msg)
