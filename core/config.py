from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Config:
    entry_cost: int
    payout_by_score: dict[int, int]
    max_score: int = 20
    min_score_payout: int = field(init=False)
    profit_by_score: dict[int, int] = field(init=False)

    def __post_init__(self):
        self.min_score_payout = min(self.payout_by_score.keys())
        self.profit_by_score = defaultdict(
            lambda: -self.entry_cost,
            {
                score: payout - self.entry_cost 
                for score, payout in self.payout_by_score.items()
            },
        )


class ConfigEnum:
    NORMALIZED = Config(
        entry_cost=1,
        payout_by_score=defaultdict(
            int,
            {
                15: 0.25,
                16: 0.5,
                17: 1,
                18: 1.25,
                19: 1.5,
                20: 2,
            },
        ),
    )
    LOW_STAKES = Config(
        entry_cost=20,
        payout_by_score=defaultdict(
            int,
            {
                15: 5,
                16: 10,
                17: 20,
                18: 25,
                19: 30,
                20: 40,
            },
        ),
    )
    HIGH_STAKES = Config(
        entry_cost=200,
        payout_by_score=defaultdict(
            int,
            {
                15: 50,
                16: 100,
                17: 200,
                18: 250,
                19: 300,
                20: 400,
            },
        ),
    )
