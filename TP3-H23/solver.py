from problem import Problem, Solution
from prim import get_root_tree
from node import TreeNode
from direction import Direction
from typing import Tuple
from indexes import neighbor_indexes, spiral_indexes
from connexe_graph import ConnexeGraph
from encloser import Encloser
import numpy as np


class Solver:
    def __init__(self, problem: Problem):
        self.problem: Problem = problem
        self.zoo: np.array = np.empty(shape=(0, 0), dtype=int)

    def solve(self) -> Solution:
        root: TreeNode = get_root_tree(self.problem)
        zoo_shape = (4 * self.problem.n, 4 * self.problem.n)
        self.zoo = -1 * np.ones(shape=zoo_shape, dtype=int)

        self.zoo = root.fill_children(self.zoo, Direction.NORTH)
        self.zoo = self.shrink_zoo()
        max_size = self.get_max_size()
        self.zoo = self.fill_zoo_with_encloser(max_size)

        for _ in range(self.problem.n):
            self.zoo = self.gravity_pull_towards_center()

        from heatmap import heatmap2d

        heatmap2d(self.zoo)
        yield Solution(self.zoo, 0)

    def insert_closest_encloser(
        self, insert_index: Tuple[int, int], middle: np.array
    ) -> np.array:
        x, y = insert_index
        middle_x, middle_y = middle
        zoo_corners = 0, self.zoo.shape[0] - 1, 0, self.zoo.shape[1] - 1

        if self.zoo[x, y] != -1:
            return self.zoo

        corners = None
        if x < middle_x and y < middle_y:
            corners = 0, x, 0, y
        elif x < middle_x and y > middle_y:
            corners = 0, x, y, zoo_corners[3]
        elif x > middle_x and y < middle_y:
            corners = x, zoo_corners[1], 0, y
        elif x > middle_x and y > middle_y:
            corners = x, zoo_corners[1], y, zoo_corners[3]

        if corners is None:
            return self.zoo

        for i, j in spiral_indexes(start_index=insert_index, corners=corners):
            if self.zoo[i, j] != -1:
                self.zoo[x, y] = self.zoo[i, j]
                self.zoo[i, j] = -1
                connexeGraph = ConnexeGraph(
                    zoo=self.zoo,
                    encloser=Encloser(
                        self.zoo[x, y], size=self.problem.size_encloser[self.zoo[x, y]]
                    ),
                    index=(x, y),
                    zoo_corners=zoo_corners,
                )
                if connexeGraph.is_connexe():
                    return self.zoo
                else:
                    self.zoo[i, j] = self.zoo[x, y]
                    self.zoo[x, y] = -1

        return self.zoo

    def encloser_reminds_connected(
        self,
        index: Tuple[int, int],
        zoo_corners: Tuple[int, int, int, int],
        value: int,
    ) -> bool:
        for i, j in neighbor_indexes(index, zoo_corners):
            if value == self.zoo[i, j]:
                return True
        return False

    def gravity_pull_towards_center(self) -> np.array:
        middle = np.array([self.zoo.shape[0] // 2, self.zoo.shape[1] // 2])

        corners = 0, self.zoo.shape[0] - 1, 0, self.zoo.shape[1] - 1

        for index in spiral_indexes(start_index=middle, corners=corners):
            self.zoo = self.insert_closest_encloser(index, middle)
        return self.zoo

    def fill_zoo_with_encloser(self, max_size: int) -> np.array:
        new_zoo_shape = (self.zoo.shape[0] * max_size, self.zoo.shape[1] * max_size)
        new_zoo = -1 * np.ones(shape=new_zoo_shape, dtype=int)

        for i in range(self.zoo.shape[0]):
            for j in range(self.zoo.shape[1]):
                if self.zoo[i, j] == -1:
                    continue
                encloser_number = self.zoo[i, j]
                encloser_size = self.problem.size_encloser[encloser_number]
                origin = np.array([i * max_size, j * max_size])
                for k in range(encloser_size):
                    new_zoo[
                        origin[0] + (k // max_size), origin[1] + (k % max_size)
                    ] = encloser_number
        return new_zoo

    def get_max_size(self) -> int:
        max_size = np.max(self.problem.size_encloser)
        max_size = np.ceil(np.log2(max_size))
        return int(max_size)

    def shrink_zoo(self) -> np.array:
        start_row_index = 0
        for i in range(self.zoo.shape[0]):
            if np.max(self.zoo[i, :]) != -1:
                start_row_index = i
                break

        end_row_index = 0
        for i in range(self.zoo.shape[0] - 1, -1, -1):
            if np.max(self.zoo[i, :]) != -1:
                end_row_index = i
                break

        start_col_index = 0
        for i in range(self.zoo.shape[1]):
            if np.max(self.zoo[:, i]) != -1:
                start_col_index = i
                break

        end_col_index = 0
        for i in range(self.zoo.shape[1] - 1, -1, -1):
            if np.max(self.zoo[:, i]) != -1:
                end_col_index = i
                break

        return self.zoo[
            start_row_index : end_row_index + 1, start_col_index : end_col_index + 1
        ]


def solve(problem: Problem) -> Solution:
    solver = Solver(problem)
    yield from solver.solve()
