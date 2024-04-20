import heapq


FLEX_POS = ['RB', 'WR', 'TE', 'D/ST', 'K']

"""
https://github.com/cwendt94/espn-api/tree/master
https://github.com/cwendt94/espn-api/wiki
"""


class HeapPlayer:
    def __init__(self, player):
        self.player = player
        self.position = player.position
        self.points = player.points
    
    def __lt__(self, other):
        return self.points > other.points

    def __eq__(self, other):
        return self.points == other.points

    def __repr__(self) -> str:
        return str(self.player)


class ActiveRoster:
    def __init__(self):
        self.roster = {
            'QB': None,
            'RB': [None, None],
            'WR': [None, None],
            'TE': None,
            'FLEX': [None, None],
            'D/ST': None,
            'K': None
        }

    @property
    def score(self):
        return sum(
            sum(y.points for y in x) if isinstance(x, list) else x.points
            for x in self.roster.values()
        )

    def __repr__(self) -> str:
        return f"""    QB:    {self._fmt_player_str(self.roster["QB"])}
    RB1:   {self._fmt_player_str(self.roster["RB"][0])}
    RB2:   {self._fmt_player_str(self.roster["RB"][1])}
    WR1:   {self._fmt_player_str(self.roster["WR"][0])}
    WR2:   {self._fmt_player_str(self.roster["WR"][1])}
    TE:    {self._fmt_player_str(self.roster["TE"])}
    FLEX1: {self._fmt_player_str(self.roster["FLEX"][0])}
    FLEX2: {self._fmt_player_str(self.roster["FLEX"][1])}
    D/ST:  {self._fmt_player_str(self.roster["D/ST"])}
    K:     {self._fmt_player_str(self.roster["K"])}"""

    @staticmethod
    def _fmt_player_str(heap_player):
        return f'{heap_player.player.name} - {heap_player.points:.3f}'

    @classmethod
    def fill_roster(cls, players):
        roster = ActiveRoster()
        player_heap = roster.build_player_heap(players)

        while not roster.is_roster_filled() and player_heap:
            curr_player = heapq.heappop(player_heap)
            pos = curr_player.position
            slot = roster.roster[pos]

            if slot is None:
                roster.roster[pos] = curr_player
            elif pos == 'RB' and not all(slot):
                roster.roster[pos][int(slot[0] is not None)] = curr_player
            elif pos == 'WR' and not all(slot):
                roster.roster[pos][int(slot[0] is not None)] = curr_player
            elif pos in FLEX_POS and not all(roster.roster['FLEX']):
                slot = roster.roster['FLEX']
                slot[int(slot[0] is not None)] = curr_player

        # If we exhaust available players and can't fill roster slot, assign zero points
        if not roster.is_roster_filled():
            for k, v in roster.roster:
                if v is None:
                    roster.roster[k] = 0.

        return roster

    @staticmethod
    def build_player_heap(players):
        player_heap = [HeapPlayer(p) for p in players]
        heapq.heapify(player_heap)

        return player_heap

    def is_roster_filled(self):
        return all(
            all(slot) if isinstance(slot, tuple) else slot is not None
            for slot in self.roster.values()
        )
