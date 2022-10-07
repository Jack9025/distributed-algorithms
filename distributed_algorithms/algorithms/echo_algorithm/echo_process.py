from threading import Thread
from . import process_manager
from ...generic.messages import MessageManager
from ...generic.process import GenericProcess


class EchoProcess(GenericProcess):
    def __init__(self, process_id: int, msg_manager: MessageManager):
        # Generic process
        super().__init__(process_id, msg_manager)

        self.decide = False  # If process has decided
        self.rec = 0  # Number of received messages
        self.father = None  # Father of process
        self.initiator = None  # If process is initiator

    def initialise(self, initiator=False):
        assert not self.initialised
        assert self.msg_manager.initialised
        assert len(self.neigh) >= 1

        self.initiator = initiator
        self.initialised = True

        # Begin executing echo algorithm
        thread = Thread(target=self.process)
        thread.start()

    def process(self):
        assert self.initialised

        if self.initiator:
            # Process is initiator
            for q in self.neigh:
                self.send(q)
            self.log(f"Sent <tok> to {', '.join(str(q) for q in self.neigh)}")

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
            self.log(f"Sent <tok> to {', '.join([str(q) for q in self.neigh if q != self.father])}")

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
