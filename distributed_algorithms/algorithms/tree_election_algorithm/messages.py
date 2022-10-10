from distributed_algorithms.generic.messages import Message


class WakeUpMessage(Message):
    def __init__(self, s_id: int):
        super().__init__(s_id)


class TokElectionMessage(Message):
    def __init__(self, s_id: int, r: int):
        super().__init__(s_id)
        self.r = r
