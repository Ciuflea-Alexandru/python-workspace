
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


def trend(swings: list[Swing]):
    #  Verifica starea trendului bazat pe 6 swinguri + un break point la al 7 lea

    if len(swings) < 7:
        return 'Date insuficiente'

    # Extragem cele 6 swinguri de baza si al 7 lea (break pointul)
    s1, s2, s3, s4, s5, s6, s7 = swings[0], swings[1], swings[2], swings[3], swings[4], swings[5], swings[6]

    # Verificam structura initiala de 6 swing-uri (3UP / 3DOWN alternativ)
    # (Poti adauga o validare suplimentara aici daca este nevoie)

    # --- CAZUL 1: UPTREND ---
    # Identificam nivelurile cheie:
    # Main kline 5(hl) si Main kline 6(hh) si Main kline 7(ll)

    mk_5 = s5['main_kline']  # hl (Higher Low)
    mk_6 = s6['main_kline']  # hh (Higher High)
    mk_7 = s7['main_kline']  # break point

    # Verificam daca este vorba despre un uptrend potential
    # (Spre exemplu, s5 și s6 respecta logica de crestere)

    # Prima posibilitate: main kline 7 < main kline 5(hl)
    if mk_7 < mk_5:
        return 'Uptrend TERMINAT (Break pointul a coborat sub HL anterior)'

    # A doua posibilitate: main kline 7 este intre main kline 5(hl) si main kline 6(hh)
    elif mk_5 <= mk_7 <= mk_6:
        return 'Uptrend IN ZONA DE DECZIE / CONSOLIDARE (Poate continua sau se poate sfarsi)'

        # --- CAZUL 2: DOWNTREND ---
        # Aici logica se inverseaza simetric pentru un downtrend de 6 swing-uri
        # Cu main kline 5(lh) si main kline 6(ll)

    return 'Trend in desfasurare'
