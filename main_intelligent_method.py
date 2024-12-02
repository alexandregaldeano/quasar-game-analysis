import json

from core.config import ConfigEnum
from core.solver import Solver


def main() -> None:
    config = ConfigEnum.NORMALIZED
    solver = Solver(config)
    policy = solver.solve()
    print(json.dumps(policy, indent=2))


if __name__ == "__main__":
    main()
