from distributed_algorithms.generic.messages import Message


class TokMessage(Message):
    def __init__(self, s_id: int, r: int):
        super().__init__(s_id)
        self.r = r

    def __str__(self):
        return f"<tok, {self.r}>"


class LdrMessage(Message):
    def __init__(self, s_id: int, r: int):
        super().__init__(s_id)
        self.r = r

    def __str__(self):
        return f"<ldr, {self.r}>"
