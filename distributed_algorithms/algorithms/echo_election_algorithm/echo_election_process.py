from enum import Enum
from threading import Thread
from .messages import TokMessage, LdrMessage
from ...generic.messages import MessageManager
from ...generic.process import GenericProcess


class State(Enum):
    SLEEP = 0
    LEADER = 1
    LOST = 2


class EchoElectionProcess(GenericProcess):
    def __init__(self, process_id: int, msg_manager: MessageManager):
        # Generic process
        super().__init__(process_id, msg_manager)

        self.decide = False  # If process has decided
        self.initiator = None  # If process is initiator

        self.caw = float('inf')  # Currently active wave
        self.rec = 0  # Number of <tok, caw> received
        self.father = None  # Father of process
        self.lrec = 0  # Number of <ldr> received
        self.win = float('inf')  # Identity of leader
        self.state = State.SLEEP  # State of process

    def initialise(self, initiator=False):
        assert not self.initialised
        assert self.msg_manager.initialised
        assert len(self.neigh) >= 1

        self.initiator = initiator
        self.decide = False  # If process has decided

        # Set to default values
        self.caw = float('inf')
        self.rec = 0
        self.father = None
        self.lrec = 0
        self.win = float('inf')
        self.state = State.SLEEP

        self.initialised = True

        # Begin executing echo election algorithm
        thread = Thread(target=self.process)
        thread.start()

    def process(self):
        assert self.initialised

        if self.initiator:
            # Process is initiator
            self.caw = self.p_id
            for q in self.neigh:
                self.send(q, TokMessage(self.caw))
            self.log(f"Sent <tok, {self.caw}> to {', '.join(str(q) for q in self.neigh)}")

        while self.lrec < len(self.neigh):
            q, msg = self.receive()
            self.log(f"Received {msg} from {q}")

            if type(msg) == LdrMessage:
                # Message is <ldr, r>
                if self.lrec == 0:
                    for s in self.neigh:
                        self.send(s, LdrMessage(msg.r))
                    self.log(f"Sent <ldr, {self.p_id}> to all neighbours "
                             f"{', '.join(str(q) for q in self.neigh)}")
                self.lrec += 1
                self.win = msg.r

            else:
                # Message is <tok, r>
                assert type(msg) == TokMessage

                if msg.r < self.caw:
                    # Reinitialise algorithm
                    self.log(f"Set caw={msg.r} (as {msg.r} < {self.caw})")
                    self.log(f"Father is {q}")
                    self.caw = msg.r
                    self.rec = 0
                    self.father = q
                    for s in [s for s in self.neigh if s != self.father]:
                        self.send(s, TokMessage(msg.r))
                    if len([s for s in self.neigh if s != self.father]) > 0:
                        self.log(f"Sent <tok, {msg.r}> to "
                                 f"{', '.join([str(s) for s in self.neigh if s != self.father])}")

                if msg.r == self.caw:
                    self.rec += 1
                    if self.rec == len(self.neigh):
                        if self.caw == self.p_id:
                            for s in self.neigh:
                                self.send(s, LdrMessage(self.p_id))
                            self.log(f"Sent <ldr, {self.p_id}> to all neighbours "
                                     f"{', '.join(str(s) for s in self.neigh)}")
                        else:
                            self.send(self.father, TokMessage(self.caw))
                            self.log(f"Sent <tok, {self.caw}> to father {self.father}")

                # if msg.r > self.caw: message is ignored

        # Set the state
        if self.win == self.p_id:
            self.state = State.LEADER
        else:
            self.state = State.LOST

        self.decide = True
        self.log(f"Decided; win={self.win}; state={self.state}")

    def __str__(self):
        return f"Process <{self.p_id}>{' (INITIATOR)' if self.initiator else ''}"
