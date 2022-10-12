from distributed_algorithms.generic.messages import Message


class WakeUpMessage(Message):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<wakeup>"


class TokElectionMessage(Message):
    def __init__(self, r: int):
        super().__init__()
        self.r = r

    def __str__(self):
        return f"<tok, {self.r}>"
