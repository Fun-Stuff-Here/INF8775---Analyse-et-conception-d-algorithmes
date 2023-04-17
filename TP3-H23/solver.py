from problem import Problem, Solution
from prim import get_filling_order
import numpy as np


def solve(problem: Problem) -> Solution:
    # TODO: implement your algorithm here
    yield Solution(get_filling_order(problem), 0)
