from dataclasses import dataclass, field
from enum import Enum

from core.config import Config


@dataclass
class ActionResult:
    score: int
    payout: int
    profit: int
    available_actions: set["ActionEnum"]


@dataclass
class Action:
    label: str
    increments: list[int]
    final: bool = field(init=False)

    def __post_init__(self):
        self.final = len(self.increments) == 0

    def apply(self, config: Config, score: int) -> set[ActionResult]:
        action_results = set()
        for increment in self.increments:
            new_score = score + increment
            payout = config.payout_by_score[new_score]
            profit = config.profit_by_score[new_score]
            available_actions = ActionEnum.available(config, new_score)
            action_results.add(ActionResult(new_score, payout, profit, available_actions))
        return action_results


class ActionEnum(Enum):
    PAYOUT = Action("payout", [])
    ONE_TO_EIGHT = Action("1-8", [1, 2, 3, 4, 5, 6, 7, 8])
    FOUR_TO_SEVEN = Action("4-7", [4, 5, 6, 7])

    @staticmethod
    def available(config: Config, score: int) -> set["ActionEnum"]:
        available_actions = set()
        if score >= config.min_score_payout:
            available_actions.add(ActionEnum.PAYOUT)
        if score <= config.max_score - min(ActionEnum.ONE_TO_EIGHT.value.increments):
            available_actions.add(ActionEnum.ONE_TO_EIGHT)
        if score <= config.max_score - min(ActionEnum.FOUR_TO_SEVEN.value.increments):
            available_actions.add(ActionEnum.FOUR_TO_SEVEN)
        return available_actions
