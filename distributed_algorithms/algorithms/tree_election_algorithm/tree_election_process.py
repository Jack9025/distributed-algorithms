from threading import Thread
from enum import Enum
from .messages import WakeUpMessage, TokElectionMessage
from ...generic.messages import MessageManager
from ...generic.process import GenericProcess


class State(Enum):
    SLEEP = 0
    LEADER = 1
    LOST = 2


class TreeElectionProcess(GenericProcess):
    def __init__(self, process_id: int, msg_manager: MessageManager):
        super().__init__(process_id, msg_manager)  # Generic process

        self.ws = False  # Wakeup started
        self.wr = 0  # Number of wakeup received
        self.rec = {}  # Record if message received from neighbour
        self.v = self.p_id  # Winner of election
        self.state = State.SLEEP  # State of process

        self.decide = False
        self.initiator = False

    def initialise(self, initiator=False):
        assert not self.initialised
        assert self.msg_manager.initialised

        self.rec = {}
        for q in self.neigh:
            # Record if p has received message from q
            self.rec[q] = False

        self.ws = False
        self.wr = 0
        self.v = self.p_id
        self.state = State.SLEEP

        self.initiator = initiator
        self.decide = False
        self.initialised = True

        # Begin executing tree election algorithm
        thread = Thread(target=self.process)
        thread.start()

    def process(self):
        assert self.initialised
        if self.initiator:
            # Process is initiator
            self.ws = True
            self.log(f"Woken up as initiator")
            for q in self.neigh:
                self.send(q, WakeUpMessage(self.p_id))
            self.log(f"Sent <wakeup> to {', '.join(str(q) for q in self.neigh)}")

        while self.wr < len(self.neigh):
            # Receive wakeup from q
            q = self.receive(msg_class=WakeUpMessage).s_id
            self.wr += 1
            self.log(f"Received <wakeup> from {q}")
            if not self.ws:
                self.ws = True
                self.log(f"Woken up")
                for q in self.neigh:
                    self.send(q, WakeUpMessage(self.p_id))
                self.log(f"Sent <wakeup> to {', '.join(str(q) for q in self.neigh)}")
        self.log(f"Received <wakeup> from all neighbours")

        # Now start the tree algorithm
        while len([q for q in self.rec if self.rec[q] is False]) > 1:
            # Receive <tok, r> from q
            msg = self.receive(msg_class=TokElectionMessage)
            self.rec[msg.s_id] = True
            self.log(f"Received <tok, {msg.r}> from {msg.s_id}")
            # Set v
            self.v = min(self.v, msg.r)

        # Now there is one q0 in rec where rec[q0] == False (silent neighbour)
        # Find q0
        q0 = None
        for n in self.rec:
            if self.rec[n] is False:
                q0 = n
                break
        assert (q0 is not None)

        # Send <tok, r> to silent neighbour q0
        self.log(f"Silent neighbour is {q0}")
        self.send(q0, TokElectionMessage(self.p_id, self.v))
        self.log(f"Sent <tok, {self.v}> to silent neighbour {q0}")

        # Receive tok from q0
        msg = self.receive(msg_class=TokElectionMessage)
        self.rec[q0] = True
        self.log(f"Received <tok, {msg.r}> from silent neighbour {q0}")

        # Now decide
        self.v = min(self.v, msg.r)
        self.decide = True
        self.log(f"Decided; v={self.v}")

        # Set state
        if self.v == self.p_id:
            self.state = State.LEADER  # Process has won
        else:
            self.state = State.LOST  # Process has lost

        # Inform other processes of decision
        if len([q for q in self.neigh if q != q0]) > 0:
            self.log(f"Informing {', '.join([str(q) for q in self.neigh if q != q0])} of decision")
        for q_star in [q for q in self.neigh if q != q0]:
            self.send(q_star, TokElectionMessage(self.p_id, self.v))

    def __str__(self):
        return f"Process <{self.p_id}>{' (INITIATOR)' if self.initiator else ''}"
