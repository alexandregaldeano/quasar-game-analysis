from core.config import Config
from core.statistics import Statistics, StatisticsForAction


class Game:
    _config: Config
    _score: int | None = None
    _statistics: Statistics

    def __init__(self, config: Config) -> None:
        self._config = config

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        self._score = value
        self._statistics = Statistics.compute_for_score(self._config, self._score)
        self._suggested_action = self._compute_suggested_action()
    
    def _compute_hint_string(self, label: str, statistics_for_action: StatisticsForAction) -> str:
        return (
            f"[{label}] "
            f"P(score > {self._config.max_score}) = {statistics_for_action.probability_above_max_score:.2f}, "
            f"E(payout) = {statistics_for_action.expected_payout:.2f}, "
            f"E(profit) = {statistics_for_action.expected_profit:.2f}"
        )
    
    def _compute_suggested_action(self, statistics: Statistics | None = None) -> str:
        if statistics is None:
            statistics = self._statistics
        suggested_action: str
        if statistics.payout.expected_profit > statistics.any_action.expected_profit:
            suggested_action = "payout"
        elif statistics.action_1_8.expected_profit == statistics.action_4_7.expected_profit:
            suggested_action = f"1—8 or 4—7 (E = {statistics.action_1_8.expected_profit:.2f})"
        elif statistics.action_1_8.expected_profit > statistics.action_4_7.expected_profit:
            suggested_action = f"1—8 (E = {statistics.action_1_8.expected_profit:.2f})"
        else:
            suggested_action = f"4—7 (E = {statistics.action_4_7.expected_profit:.2f})"
        return suggested_action

    def print_hints_for_score(self):
        print(self._compute_hint_string("1—8", self._statistics.action_1_8))
        print(self._compute_hint_string("4—7", self._statistics.action_4_7))
        print(self._compute_hint_string("any", self._statistics.any_action))
        print(self._compute_hint_string("payout", self._statistics.payout))
        print(f"Suggested action: {self._suggested_action}")
        
    def print_all_hints(self, debug=False):
        for score in range(1, self._config.max_score + 1):
            statistics = Statistics.compute_for_score(self._config, score)
            if debug:
                print(f"Score: {score}")
                print(f"[1—8] {statistics.action_1_8.expected_profit}")
                print(f"[4—7] {statistics.action_4_7.expected_profit}")
                print(f"[payout] {statistics.payout.expected_profit}")
            else:
                print(f"[{score}] {self._compute_suggested_action(statistics)}")