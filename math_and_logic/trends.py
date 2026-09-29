
class Kline:
    def __init__(self, id, high, low, open, close, volume):
        self.id = int
        self.high = float
        self.low = float
        self.open = float
        self.close = float
        self.volume = float


class Swing:
    def __init__(self, klines: list[Kline], direction: str) -> None:
        self.klines = klines
        self.direction = direction  # up down consolidate

    def main_kline_index(self):
        return len(self.klines) // 2

    def prise_boundaries(self) -> tuple[float, float]:
        if self.direction == "UP":
            return self.klines[self.main_kline_index()].low, self.klines[self.main_kline_index()].close
        elif self.direction == "DOWN":
            pass
        else:
            # CONSOLIDATE
            return min([k.low for k in self.klines]), max([k.high for k in self.klines])
