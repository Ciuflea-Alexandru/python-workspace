
class Kline:
    def __init__(self, id, high, low, open, close, volume):
        self.id = int(id)
        self.high = float(high)
        self.low = float(low)
        self.open = float(open)
        self.close = float(close)
        self.volume = float(volume)


class Swing:
    def __init__(self, klines: list[Kline], direction: str) -> None:
        self.klines = klines
        self.direction = direction  # up down consolidate

    def main_kline_index(self):
        return len(self.klines) // 2

    def price_boundaries(self) -> tuple[float, float] | None:
        if self.direction == 'UP':
            return self.klines[self.main_kline_index()].low, self.klines[self.main_kline_index()].close
        elif self.direction == 'DOWN':
            return self.klines[self.main_kline_index()].high, self.klines[self.main_kline_index()].close
        else:
            # CONSOLIDATE( I will work on this later)
            return min([k.low for k in self.klines]), max([k.high for k in self.klines])


def group_swings(klines: list[Kline]) -> list[Swing]:
    if not klines:
        return []

    swings = []
    current_group = []
    current_direction = None

    pending_opposite = []
    opposite_direction = None

    for kline in klines:
        # Determina directia lumanari curente bazata pe close/open
        if kline.close > kline.open:
            kline_dir = 'UP'
        elif kline.close < kline.open:
            kline_dir = 'DOWN'
        else:
            kline_dir = 'FLAT'

        # Daca e prima lumanare sau continua aceeasi directie
        if current_direction is None:
            current_direction = kline_dir
            current_group.append(kline)
        elif kline_dir == current_direction or kline_dir == 'FLAT':
            # In caz de fakeout sterge valorile din pending
            if pending_opposite:
                current_group.extend(pending_opposite)
                pending_opposite = []
                opposite_direction = None

            current_group.append(kline)
        else:
            # Lumanare de directie opusa
            if opposite_direction is None:
                opposite_direction = kline_dir
                pending_opposite = [kline]
            elif kline_dir == opposite_direction:
                pending_opposite.append(kline)

            # Verificam daca s-au strans 3 kline-uri opuse consecutive
            if len(pending_opposite) >= 3 and opposite_direction in ('UP', 'DOWN'):
                # Salvam grupul anterior daca are cel putin 3 elemente
                if len(current_group) >= 3 and current_direction in ('UP', 'DOWN'):
                    swings.append(Swing(current_group, current_direction))

                # Pornim un nou grup cu cele 3 lumanari si schimbam directia
                current_group = pending_opposite
                current_direction = opposite_direction
                pending_opposite = []
                opposite_direction = None

    # Daca au ramas lumanari in pending la final sunt considerate fakeout si se adauga la ultimul grup
    if pending_opposite:
        current_group.extend(pending_opposite)

    # Pastreaza ultimul grup ramas in memorie
    if len(current_group) >= 3 and current_direction in ('UP', 'DOWN'):
        swings.append(Swing(current_group, current_direction))

    return swings


class Trend:
    def __init__(self, swings: list[Swing]):
        self.swings = swings

    @staticmethod  # Am decis sa fac functia statica ca sa o pastrez in clasa trend
    def get_main_kline(swing: Swing) -> float:
        # Returneaza valoarea main klineului pentru un swing
        idx = swing.main_kline_index()
        return swing.klines[idx].close

    def evaluate(self):
        # Avem nevoie de cel putin 7 swinguri (6 pentru structura + 1 break point)
        if len(self.swings) < 7:
            return 'Date insuficiente (necesare cel puțin 7 swing-uri)'

        # Extragem valorile main kline pentru primele 6 swinguri
        mk = [self.get_main_kline(s) for s in self.swings[:6]]
        s1, s2, s3, s4, s5, s6 = mk[0], mk[1], mk[2], mk[3], mk[4], mk[5]

        # Al 7 lea swing este break pointul
        mk_7 = self.get_main_kline(self.swings[6])

        # 1. VERIFICARE UPTREND
        if s1 > s2 < s3 > s4 < s5 > s6:
            # Structura de 6 swinguri este valia
            # Acum verificam break pointul (s7 / mk_7) fata de s5 (hl) si s6 (hh)
            hl = s5
            hh = s6

            if mk_7 < hl:
                return 'Uptrend TERMINAT (Break pointul a coborat sub HL anterior)'
            elif hl <= mk_7 <= hh:
                return 'Uptrend in zona de CONSOLIDARE'
            else:
                return 'Uptrend in continuare'

        # VERIFICARE DOWNTREND
        elif s1 < s2 > s3 < s4 > s5 < s6:
            lh = s5
            ll = s6

            if mk_7 > lh:
                return 'Downtrend TERMINAT (Break pointul a urcat peste LH anterior)'
            elif ll <= mk_7 <= lh:
                return 'Downtrend CONSOLIDARE'
            else:
                return 'Downtrend in continuare'

        return 'Fara trend clar'
