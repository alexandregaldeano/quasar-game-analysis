import numpy as np
from mdptoolbox import mdp

from core.action import ActionEnum
from core.config import Config


class Solver:
    config: Config
    initial_score: int = 1
    max_possible_score: int
    number_of_scores: int
    actions = list(ActionEnum)
    available_actions_by_score: dict[int, set[ActionEnum]]
    scores: list[int]

    def __init__(self, config: Config) -> None:
        self.config = config
        self.scores = list(range(self.initial_score, self.config.max_score + 1))
        self.available_actions_by_score = {score: ActionEnum.available(self.config, score) for score in self.scores}

    def _build_transitions(self) -> np.ndarray:
        number_of_scores = len(self.scores)
        number_of_actions = len(self.actions)
        # Add a state for the score > max_score and the final state
        transitions = np.zeros((number_of_actions, number_of_scores + 2, number_of_scores + 2))
        for action_index, action in enumerate(self.actions):
            for from_score_index, from_score in enumerate(self.scores):
                if action.value.final or action not in self.available_actions_by_score[from_score]:
                    # If the action is unavailable, end of the game
                    transitions[action_index, from_score_index, -1] = 1
                    continue
                if action.value.final:
                    transitions[action_index, from_score_index, -1] = 1
                    continue
                transition_probability = 1 / len(action.value.increments)
                for increment in action.value.increments:
                    to_score = from_score + increment
                    if to_score > self.config.max_score:
                        to_score_index = -2
                    else:
                        to_score_index = self.scores.index(to_score)
                    transitions[action_index, from_score_index, to_score_index] += transition_probability
            # When the score is greater than the max score, end of the game
            transitions[action_index, -2, -1] = 1
            # All actions loop in the final state
            transitions[action_index, -1, -1] = 1
        return transitions

    def _build_reward(self) -> np.ndarray:
        number_of_scores = len(self.scores)
        number_of_actions = len(self.actions)
        reward = np.zeros((number_of_scores + 2, number_of_actions))
        for action_index, action in enumerate(self.actions):
            for score_index, score in enumerate(self.scores):
                if action not in self.available_actions_by_score[score]:
                    reward[score_index, action_index] = -np.inf
                    continue
                if not action.value.final:
                    continue
                reward[score_index, action_index] = self.config.profit_by_score[score]
            # When the score is greater than the max score, only the final action is available
            if action.value.final:
                reward[-2, action_index] = self.config.profit_by_score[self.config.max_score + 1]
            else:
                reward[-2, action_index] = -np.inf
        return reward

    def solve(self, discount=1, epsilon=0.0001, max_iter=100000) -> dict[int, ActionEnum]:
        transitions = self._build_transitions()
        reward = self._build_reward()
        solver = mdp.ValueIteration(
            transitions=transitions,
            reward=reward,
            discount=discount,
            epsilon=epsilon,
            max_iter=max_iter,
        )
        solver.run()
        return {
            score: self.actions[solver.policy[score_index]].value.label
            for score_index, score in enumerate(self.scores)
            if score <= self.config.max_score
        }
