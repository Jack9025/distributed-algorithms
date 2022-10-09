from .messages import MessageManager, Message


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

    def receive(self, msg_class=Message) -> Message:
        """Gets the message received by the process"""
        while not self.msg_manager.has_message(self.p_id, msg_class):
            # Wait until p has received message
            pass

        # Fetch and return message for p
        return self.msg_manager.fetch_message(self.p_id, msg_class)

    def send(self, q_id: int, msg: Message = None):
        """Sends a message to process q"""
        if not msg:
            # Default to basic message with p_id
            msg = Message(self.p_id)
        self.msg_manager.add_message(q_id, msg)

    def log(self, msg: str):
        """Logs a message"""
        self.msg_manager.log(f"{self}: {msg}")

    def __str__(self):
        return f"Process <{self.p_id}>"
