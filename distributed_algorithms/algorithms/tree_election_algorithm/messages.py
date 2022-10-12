from distributed_algorithms.generic.messages import Message


class WakeUpMessage(Message):
    def __init__(self):
        super().__init__()


class TokElectionMessage(Message):
    def __init__(self, r: int):
        super().__init__()
        self.r = r
