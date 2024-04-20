from espn_api.football.box_score import BoxScore

from .roster import ActiveRoster


class LeagueWeek:
    def __init__(self, box_scores: list[BoxScore]):
        self.matchups = [
            Matchup(b)
            for b in box_scores
        ]

    def __repr__(self) -> str:
        return f'\n{"-" *20}\n{"-" * 20}\n'.join(
            self._fmt_matchup_str(matchup) for matchup in self.matchups
        )

    @staticmethod
    def _fmt_matchup_str(matchup):
        return '\n'.join((
            f'Home Team: {matchup.home_team}: {matchup.home_score:.3f} pts',
            str(matchup.home_lineup),
            '-' * 10,
            f'Away Team: {matchup.away_team}: {matchup.away_score:.3f} pts',
            str(matchup.away_lineup)    
        ))



class Matchup:
    def __init__(self, box_score):
        self.home_team = box_score.home_team
        self.home_lineup = ActiveRoster.fill_roster(box_score.home_lineup)
        self.home_score = self.home_lineup.score

        self.away_team = box_score.away_team
        self.away_lineup = ActiveRoster.fill_roster(box_score.away_lineup)
        self.away_score = self.away_lineup.score
