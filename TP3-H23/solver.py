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

    from heatmap import heatmap2d

    heatmap2d(zoo)

    yield Solution(zoo, 0)


def shrink_zoo(zoo):
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
