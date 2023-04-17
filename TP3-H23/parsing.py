import argparse
import numpy as np
from problem import Problem, Solution
from solver import solve


def parse_file(file_name: str) -> Problem:
    with open(file_name, "r") as file:
        n, m, k = [int(x) for x in file.readline().split()]
        # index bonus
        index_bonus = np.array([int(x) for x in file.readline().split()])
        size_encloser = np.array([int(file.readline()) for _ in range(n)])
        # edge matrix
        edge_matrix = np.array(
            [[int(x) for x in file.readline().split()] for _ in range(n)]
        )

    return Problem(n, m, k, index_bonus, size_encloser, edge_matrix)


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", dest="e", type=str, help="e: Path to the exemple")
    parser.add_argument(
        "-p", dest="p", type=bool, help="p: print the matrix", default=False, nargs="?"
    )
    args = parser.parse_args()

    if args.p is None:
        args.p = True

    problem = parse_file(args.e)

    final_solution: Solution = Solution(np.array([]), 0)

    for i, solution in enumerate(solve(problem)):
        # TODO : afficher le zoo avec l'attrait de chaque enclos
        final_solution = solution
        if args.p:
            print(
                f"{i} : solution {solution.zoo} with attraction {solution.attraction}"
            )
