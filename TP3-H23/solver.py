from problem import Problem, Solution
from prim import get_root_tree
from node import TreeNode
from direction import Direction
import numpy as np


def solve(problem: Problem) -> Solution:
    # TODO: implement your algorithm here
    root: TreeNode = get_root_tree(problem)
    zoo_shape = (5 * problem.n, 5 * problem.n)
    zoo = -1 * np.ones(shape=zoo_shape, dtype=int)

    zoo = root.fill_children(zoo, Direction.NORTH)

    from heatmap import heatmap2d

    heatmap2d(zoo)

    yield Solution(zoo, 0)
