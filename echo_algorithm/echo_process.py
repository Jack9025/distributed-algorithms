from threading import Thread
from . import process_manager
from .process_manager import MessageManager


class EchoProcess:
    def __init__(self, process_id: int, msg_manager: MessageManager):
        self.p_id = process_id  # ID of current process
        self.decide = False  # If process has decided
        self.rec = 0  # Number of received messages
        self.father = None

        # Process specific
        self.msg_manager = msg_manager
        self.neigh = []  # Neighbours
        self.initiator = None

        self.initialised = False

    def initialise(self, neighbours, initiator=False):
        assert not self.initialised
        assert self.msg_manager.initialised

        self.neigh = neighbours
        self.initiator = initiator
        self.initialised = True

        # Begin executing echo algorithm
        thread = Thread(target=self.process)
        thread.start()

    def receive(self) -> int:
        while not self.msg_manager.has_message(self.p_id):
            # Wait until p has received message
            pass

        # Fetch and return message for p
        return self.msg_manager.fetch_message(self.p_id)

    def send(self, q):
        self.msg_manager.add_message(self.p_id, q)

    def process(self):
        assert self.initialised

        if self.initiator:
            # Process is initiator
            for q in self.neigh:
                self.send(q)
                self.log(f"Sent <tok> to {q}")

            while self.rec < len(self.neigh):
                q = self.receive()
                self.rec += 1
                self.log(f"Received <tok> from {q}")

            self.decide = True
            self.log("Decided")

        else:
            # Process is non-initiator
            q = self.receive()
            self.father = q
            self.rec += 1
            self.log(f"Received <tok> from father {q}")

            for q in [q for q in self.neigh if q != self.father]:
                self.send(q)
                self.log(f"Sent <tok> to {q}")

            while self.rec < len(self.neigh):
                q = self.receive()
                self.rec += 1
                self.log(f"Received <tok> from {q}")

            self.log(f"Received <tok> from all neighbours")

            self.send(self.father)
            self.log(f"Sent <tok> to father {self.father}")

    def log(self, msg: str):
        process_manager.log(f"{self}: {msg}")

    def __str__(self):
        return f"Process <{self.p_id}>{' (INITIATOR)' if self.initiator else ''}"
