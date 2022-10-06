from threading import Thread
from . import process_manager
from ...generic.messages import MessageManager


class Process:
    def __init__(self, process_id: int, msg_manager: MessageManager):
        self.p_id = process_id  # ID of current process
        self.decide = False  # If process has decided
        self.rec = {}
        self.neigh = []

        # Process specific
        self.msg_manager = msg_manager

        # Tree attributes for parent and children
        self.parent = None
        self.children = []

        self.initialised = False

    def initialise(self):
        assert not self.initialised
        assert self.msg_manager.initialised

        for q in self.get_neigh():
            # Record if p has received message from q
            self.rec[q] = False

        self.neigh = self.get_neigh()

        self.initialised = True

        # Begin executing tree algorithm
        thread = Thread(target=self.process)
        thread.start()

    def set_parent(self, node):
        self.parent = node

    def add_child(self, node):
        self.children += [node]

    def get_neigh(self):
        neigh = []
        if self.parent:
            neigh += [self.parent.p_id]
        neigh += [q.p_id for q in self.children]
        return neigh

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

        while len([q for q in self.rec if self.rec[q] is False]) > 1:
            # Receive tok from q
            q = self.receive()
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

    def log(self, msg: str):
        process_manager.log(f"{self}: {msg}")

    def __str__(self):
        return f"Process <{self.p_id}>"
