import heapq
from pprint import pprint


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

    def __repr__(self) -> str:
        return '\n'.join(f'{k}: {v.player}' for k, v in self.roster.items())

    def fill_roster(self, players):
        player_heap = self.build_player_heap(players)

        while not self.is_roster_filled() and player_heap:
            curr_player = heapq.heappop(player_heap)
            pos = curr_player.position
            slot = self.roster[pos]

            if slot is None:
                self.roster[pos] = curr_player
            elif pos == 'RB' and not all(slot):
                self.roster[pos][int(slot[0] is not None)] = curr_player
            elif pos == 'WR' and not all(slot):
                self.roster[pos][int(slot[0] is not None)] = curr_player
            elif pos in FLEX_POS and not all(self.roster['FLEX']):
                slot = self.roster['FLEX']
                slot[int(slot[0] is not None)] = curr_player

        # If we exhaust available players and can't fill roster slot, assign zero points
        if not self.is_roster_filled:
            for k, v in self.roster:
                if v is None:
                    self.roster[k] = 0.

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
