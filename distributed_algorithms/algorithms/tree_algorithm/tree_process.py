from threading import Thread
from ...generic.messages import MessageManager
from ...generic.process import GenericProcess


class TreeProcess(GenericProcess):
    def __init__(self, process_id: int, msg_manager: MessageManager):
        super().__init__(process_id, msg_manager)  # Generic process

        self.rec = {}  # Record if message received from neighbour
        self.decide = False  # If process has decided

    def initialise(self):
        assert not self.initialised
        assert self.msg_manager.initialised

        self.rec = {}
        for q in self.neigh:
            # Record if p has received message from q
            self.rec[q] = False

        self.decide = False
        self.initialised = True

        # Begin executing tree algorithm
        thread = Thread(target=self.process)
        thread.start()

    def process(self):
        assert self.initialised

        while len([q for q in self.rec if self.rec[q] is False]) > 1:
            # Receive tok from q
            q, msg = self.receive()
            self.rec[q] = True
            self.log(f"Received <tok> from {q}")

        # Now there is one q0 in rec where rec[q0] == False (silent neighbour)
        # Find q0
        q0 = None
        for n in self.rec:
            if self.rec[n] is False:
                q0 = n
                break
        assert (q0 is not None)

        self.log(f"Silent neighbour is {q0}")
        self.send(q0)
        self.log(f"Sent <tok> to silent neighbour {q0}")

        # Receive tok from q
        self.receive()
        self.rec[q0] = True
        self.log(f"Received <tok> from silent neighbour {q0}")

        # Now decide
        self.decide = True
        self.log(f"Decided")

        # Inform other processes of decision
        if len([q for q in self.neigh if q != q0]) > 0:
            self.log(f"Informing {', '.join([str(q) for q in self.neigh if q != q0])} of decision")
        for q_star in [q for q in self.neigh if q != q0]:
            self.send(q_star)
