from distributed_algorithms.generic.messages import Message


class TokMessage(Message):
    def __init__(self, r: int):
        super().__init__()
        self.r = r

    def __str__(self):
        return f"<tok, {self.r}>"


class LdrMessage(Message):
    def __init__(self, r: int):
        super().__init__()
        self.r = r

    def __str__(self):
        return f"<ldr, {self.r}>"
