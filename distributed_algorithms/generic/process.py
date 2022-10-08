from .messages import MessageManager


class GenericProcess:
    def __init__(self, process_id: int, msg_manager: MessageManager):
        self.p_id = process_id  # ID of current process
        self.msg_manager = msg_manager  # Message manager
        self.neigh = []  # Neighbours of current process
        self.initialised = False  # Not yet initialised

    def add_neigh(self, neigh: int):
        """Adds neighbour to neighbours of process"""
        assert neigh not in self.neigh
        self.neigh.append(neigh)

    def receive(self) -> int:
        """Gets the process ID of the message received"""
        while not self.msg_manager.has_message(self.p_id):
            # Wait until p has received message
            pass

        # Fetch and return message for p
        return self.msg_manager.fetch_message(self.p_id)

    def send(self, q_id: int):
        """Sends a message to a process"""
        self.msg_manager.add_message(self.p_id, q_id)

    def log(self, msg: str):
        """Logs a message"""
        self.msg_manager.log(f"{self}: {msg}")

    def __str__(self):
        return f"Process <{self.p_id}>"
