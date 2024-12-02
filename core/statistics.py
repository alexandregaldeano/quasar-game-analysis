from dataclasses import dataclass

from core.config import Config


@dataclass
class StatisticsForAction:  
    probability_above_max_score: float
    expected_payout: float
    expected_profit: float
    
@dataclass
class Statistics:
    action_1_8: StatisticsForAction
    action_4_7: StatisticsForAction
    any_action: StatisticsForAction
    payout: StatisticsForAction

    @staticmethod
    def compute_for_score(config: Config, score: int) -> "Statistics":
        action_1_8 = Statistics._compute_statistics_for_action(config, score, 1, 8)
        action_4_7 = Statistics._compute_statistics_for_action(config, score, 4, 7)
        any_action = StatisticsForAction(
            (action_1_8.probability_above_max_score + action_4_7.probability_above_max_score) / 2,
            (action_1_8.expected_payout + action_4_7.expected_payout) / 2,
            (action_1_8.expected_profit + action_4_7.expected_profit) / 2,
            )
        payout = Statistics._compute_statistics_for_action(config, score, 0, 0)
        return Statistics(action_1_8, action_4_7, any_action, payout)

    @staticmethod
    def _compute_statistics_for_action(
        config: Config,
        score: int,
        increment_min: int,
        increment_max: int,
    ) -> StatisticsForAction:
        increment_range = increment_max - increment_min + 1
        probability_above_max_score = sum(
            1
            for increment in range(increment_min, increment_max+1)
            if score + increment > config.max_score
        ) / increment_range
        expected_payout = sum(
            config.payout_by_score[score + increment]
            for increment in range(increment_min, increment_max+1)
        ) / increment_range
        expected_profit = sum(
            config.profit_by_score[score + increment]
            for increment in range(increment_min, increment_max+1)
        ) / increment_range
        return StatisticsForAction(probability_above_max_score, expected_payout, expected_profit)