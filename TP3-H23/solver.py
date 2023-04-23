from problem import Problem, Solution
from prim import get_root_tree
from node import TreeNode
from direction import Direction
import numpy as np


def solve(problem: Problem) -> Solution:
    # TODO: implement your algorithm here
    root: TreeNode = get_root_tree(problem)
    zoo_shape = (4 * problem.n, 4 * problem.n)
    zoo = -1 * np.ones(shape=zoo_shape, dtype=int)

    zoo = root.fill_children(zoo, Direction.NORTH)
    zoo = shrink_zoo(zoo)
    max_size = get_max_size(problem)
    zoo = fill_zoo_with_encloser(problem, zoo, max_size)

    # zoo = squish_along_axis(zoo, max_size, axis=0)

    from heatmap import heatmap2d

    heatmap2d(zoo)
    yield Solution(zoo, 0)


def squish_along_axis(zoo: np.array, max_size: int, axis: int = 0) -> np.array:
    for j in range(zoo.shape[axis] // max_size):
        inspect_index = 0
        insert_index = 0
        origin = j * max_size
        while inspect_index < zoo.shape[axis]:
            if np.max(zoo[inspect_index, origin : origin + max_size]) != -1:
                for k in range(max_size):
                    zoo[insert_index, origin + k] = zoo[inspect_index, origin + k]
                    zoo[inspect_index, origin + k] = -1
                insert_index += 1
            inspect_index += 1
    return zoo


def fill_zoo_with_encloser(problem: Problem, zoo: np.array, max_size: int) -> np.array:
    new_zoo_shape = (zoo.shape[0] * max_size, zoo.shape[1] * max_size)
    new_zoo = -1 * np.ones(shape=new_zoo_shape, dtype=int)

    for i in range(zoo.shape[0]):
        for j in range(zoo.shape[1]):
            if zoo[i, j] == -1:
                continue
            encloser_number = zoo[i, j]
            encloser_size = problem.size_encloser[encloser_number]
            origin = np.array([i * max_size, j * max_size])
            for k in range(encloser_size):
                new_zoo[
                    origin[0] + (k // max_size), origin[1] + (k % max_size)
                ] = encloser_number
    return new_zoo


def get_max_size(problem: Problem) -> int:
    max_size = np.max(problem.size_encloser)
    max_size = np.ceil(np.log2(max_size))
    return int(max_size)


def shrink_zoo(zoo: np.array) -> np.array:
    start_row_index = 0
    for i in range(zoo.shape[0]):
        if np.max(zoo[i, :]) != -1:
            start_row_index = i
            break

    end_row_index = 0
    for i in range(zoo.shape[0] - 1, -1, -1):
        if np.max(zoo[i, :]) != -1:
            end_row_index = i
            break

    start_col_index = 0
    for i in range(zoo.shape[1]):
        if np.max(zoo[:, i]) != -1:
            start_col_index = i
            break

    end_col_index = 0
    for i in range(zoo.shape[1] - 1, -1, -1):
        if np.max(zoo[:, i]) != -1:
            end_col_index = i
            break

    return zoo[start_row_index : end_row_index + 1, start_col_index : end_col_index + 1]
