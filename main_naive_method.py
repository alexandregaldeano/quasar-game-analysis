import argparse

from core.config import ConfigEnum
from core.game import Game


def main() -> None:
    config = ConfigEnum.NORMALIZED
    game = Game(config)
    game.print_all_hints(debug=True)
    while True:
        input_str = input("Enter score: ")
        if input_str == "q":
            break
        game.score = int(input_str)
        game.print_hints_for_score()

if __name__ == "__main__":
    main()