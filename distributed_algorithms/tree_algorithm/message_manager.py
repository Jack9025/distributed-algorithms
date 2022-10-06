class MessageManager:
    def __init__(self):
        self.processes = []
        self.messages = {}
        self.initialised = False

    def initialise(self, processes):
        assert len(processes) >= 2
        assert not self.initialised

        self.processes = processes
        self.messages = {}
        for process in processes:
            self.messages[process.p_id] = []

        self.initialised = True

    def has_message(self, p_id: int):
        """Checks if p has received a message"""
        assert (p_id in self.messages)
        return len(self.messages[p_id]) >= 1

    def fetch_message(self, p_id: int):
        """Fetches process ids of messages sent to p"""
        assert (self.has_message(p_id))
        msg = self.messages[p_id][0]
        del self.messages[p_id][0]
        return msg

    def add_message(self, p_id: int, q_id: int):
        """Adds message from p_id to q_id"""
        self.messages[q_id].append(p_id)
