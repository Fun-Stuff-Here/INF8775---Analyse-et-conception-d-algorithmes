import argparse
import numpy as np
from problem import Problem, Solution
from solver import solve
from itertools import combinations
import time


def distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


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
        final_solution = solution
        enclos: dict = dict()
        for index in np.ndindex(solution.zoo.shape):
            if solution.zoo[index] == -1:
                continue
            if solution.zoo[index] not in enclos:
                enclos[solution.zoo[index]] = []
            enclos[solution.zoo[index]].append(index)
        if args.p:
            for i in range(problem.n):
                print(" ".join([f"{str(x)} {str(y)}" for x, y in enclos[i]]))
        else:
            # Évaluation de la solution
            # somme de tous les poids
            sol = [enclos[i] for i in range(problem.n)]
            poids = problem.edge_matrix
            theme = problem.index_bonus
            m = problem.m
            k = problem.k
            n = problem.n
            distances = [[9999 for _ in sol] for _ in sol]
            combs_enclos = combinations(range(len(sol)), 2)
            for paire in combs_enclos:
                for start in sol[paire[0]]:
                    for end in sol[paire[1]]:
                        lenght = distance(start[0], start[1], end[0], end[1])
                        if lenght < distances[paire[0]][paire[1]]:
                            distances[paire[0]][paire[1]] = lenght
                            distances[paire[1]][paire[0]] = lenght

            somme = 0
            for i, _ in enumerate(sol):
                for j, _ in enumerate(sol):
                    somme += poids[i][j] * distances[i][j]

            # vérifier la contrainte de distance
            combs_theme = combinations(theme, 2)
            bonus = m**2
            for paire in combs_theme:
                if distances[paire[0]][paire[1]] > k:
                    bonus = 0
                    break
            print(f"{bonus - somme}")
    time.sleep(120)  # to satisfy that the program needs to be interrupted manually
