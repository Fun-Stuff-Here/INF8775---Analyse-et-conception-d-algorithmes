from problem import Problem, Solution
from prim import get_root_tree
from node import TreeNode
from direction import Direction
from typing import Tuple, List
from indexes import neighbor_indexes, spiral_indexes
from connexe_graph import ConnexeGraph
from encloser import Encloser
from time import perf_counter
from heatmap import heatmap2d
import numpy as np
import copy


class Solver:
    def __init__(self, problem: Problem):
        self.problem: Problem = problem
        self.zoo: np.array = np.empty(shape=(0, 0), dtype=int)
        max_size = np.max(self.problem.size_encloser)
        max_size = np.ceil(np.log2(max_size))
        self.max_size = int(max_size)

    def solve(self) -> Solution:
        start = perf_counter()
        root: TreeNode = get_root_tree(self.problem)
        zoo_shape = (4 * self.problem.n, 4 * self.problem.n)
        self.zoo = -1 * np.ones(shape=zoo_shape, dtype=int)

        self.zoo = root.fill_children(self.zoo, Direction.NORTH)
        self.zoo = self.shrink_zoo()
        self.zoo = self.fill_zoo_with_encloser()
        self.zoo = self.squash(0)
        self.zoo = self.squash(1)
        self.zoo = self.shrink_zoo()

        middle = np.array([self.zoo.shape[0] // 2, self.zoo.shape[1] // 2])
        for direction in [
            Direction.NORTH_EAST,
            Direction.NORTH_WEST,
            Direction.SOUTH_EAST,
            Direction.SOUTH_WEST,
        ]:
            index = middle[0] + direction[0], middle[1] + direction[1]
            self.zoo = self.gravity_pull_towards_center(index)

        end = perf_counter()
        print(f"Time: {end - start} s")

        heatmap2d(self.zoo)
        yield Solution(self.zoo, 0)

    def squash(self, axis: int) -> np.array:
        middle = np.array([self.zoo.shape[0] // 2, self.zoo.shape[1] // 2])
        visited: set = set()
        zoo_corners = 0, self.zoo.shape[0] - 1, 0, self.zoo.shape[1] - 1
        for index in spiral_indexes(start_index=middle, corners=zoo_corners):
            if self.zoo[index] == -1 or self.zoo[index] in visited:
                continue
            visited.add(self.zoo[index])
            coordinates: List[Tuple[int, int]] = ConnexeGraph(
                zoo=self.zoo,
                encloser=Encloser(
                    self.zoo[index], size=self.problem.size_encloser[self.zoo[index]]
                ),
                index=index,
                zoo_corners=zoo_corners,
            ).get_coordinates()

            new_coordinates = copy.deepcopy(coordinates)
            new_coordinates_try = new_coordinates
            while self.is_fitting(
                encloser_number=self.zoo[index],
                coordinates=new_coordinates_try,
                corners=zoo_corners,
            ):
                direction_above = Direction.NORTH if axis == 1 else Direction.EAST
                direction_below = Direction.SOUTH if axis == 1 else Direction.WEST
                new_coordinates = copy.deepcopy(new_coordinates_try)

                coords = [coordinate[axis] for coordinate in new_coordinates]
                extremum = (
                    np.min(coords) if coords[0] > middle[axis] else np.max(coords)
                )

                if abs(extremum - middle[axis]) < self.max_size // 2:
                    break

                direction = (
                    direction_above if extremum < middle[axis] else direction_below
                )
                new_coordinates_try = [
                    (
                        coordinate[0] + direction[0],
                        coordinate[1] + direction[1],
                    )
                    for coordinate in new_coordinates
                ]
            value = self.zoo[index]
            for coordinate in coordinates:
                if coordinate not in new_coordinates:
                    self.zoo[coordinate] = -1
            for coordinate in new_coordinates:
                self.zoo[coordinate] = value
        return self.zoo

    def is_fitting(
        self,
        encloser_number: int,
        coordinates: List[Tuple[int, int]],
        corners: Tuple[int, int, int, int],
    ):
        min_x, max_x, min_y, max_y = corners
        for x, y in coordinates:
            if x < min_x or x > max_x or y < min_y or y > max_y:
                return False
            if self.zoo[x, y] != -1 and self.zoo[x, y] != encloser_number:
                return False
        return True

    def insert_closest_encloser(
        self, insert_index: Tuple[int, int], middle: np.array
    ) -> np.array:
        x, y = insert_index
        if self.zoo[x, y] != -1:
            return self.zoo

        middle_x, middle_y = middle
        zoo_corners = 0, self.zoo.shape[0] - 1, 0, self.zoo.shape[1] - 1

        corners = self.corners_for_cadran(x, y, middle_x, middle_y, zoo_corners)

        if corners is None:
            return self.zoo

        for i, j in spiral_indexes(
            start_index=insert_index, corners=corners, max_radius=self.max_size // 2
        ):
            if self.zoo[i, j] == -1:
                continue
            self.zoo[x, y] = self.zoo[i, j]
            self.zoo[i, j] = -1

            if ConnexeGraph(
                zoo=self.zoo,
                encloser=Encloser(
                    self.zoo[x, y], size=self.problem.size_encloser[self.zoo[x, y]]
                ),
                index=(x, y),
                zoo_corners=zoo_corners,
            ).is_connexe():
                return self.zoo
            else:
                self.zoo[i, j] = self.zoo[x, y]
                self.zoo[x, y] = -1

        return self.zoo

    def corners_for_cadran(self, x, y, middle_x, middle_y, zoo_corners):
        corners = None
        if x <= middle_x and y <= middle_y:
            corners = 0, x, 0, y
        elif x <= middle_x and y >= middle_y:
            corners = 0, x, y, zoo_corners[3]
        elif x >= middle_x and y <= middle_y:
            corners = x, zoo_corners[1], 0, y
        elif x >= middle_x and y >= middle_y:
            corners = x, zoo_corners[1], y, zoo_corners[3]
        return corners

    def gravity_pull_towards_center(self, middle: np.array) -> np.array:
        corners = 0, self.zoo.shape[0] - 1, 0, self.zoo.shape[1] - 1

        for index in spiral_indexes(start_index=middle, corners=corners):
            self.zoo = self.insert_closest_encloser(index, middle)
        return self.zoo

    def fill_zoo_with_encloser(self) -> np.array:
        new_zoo_shape = (
            self.zoo.shape[0] * self.max_size,
            self.zoo.shape[1] * self.max_size,
        )
        new_zoo = -1 * np.ones(shape=new_zoo_shape, dtype=int)

        for i in range(self.zoo.shape[0]):
            for j in range(self.zoo.shape[1]):
                if self.zoo[i, j] == -1:
                    continue
                encloser_number = self.zoo[i, j]
                encloser_size = self.problem.size_encloser[encloser_number]
                origin = np.array([i * self.max_size, j * self.max_size])
                for k in range(encloser_size):
                    new_zoo[
                        origin[0] + (k // self.max_size),
                        origin[1] + (k % self.max_size),
                    ] = encloser_number
        return new_zoo

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
