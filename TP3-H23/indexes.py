from typing import Tuple, Optional
from direction import Direction
from functools import lru_cache
import numpy as np


def neighbor_indexes(
    index: Tuple[int, int], zoo_corners: Tuple[int, int, int, int]
) -> Tuple[int, int]:
    min_x, max_x, min_y, max_y = zoo_corners

    for direction in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
        i, j = index + direction
        if i < min_x or i > max_x or j < min_y or j > max_y:
            continue
        yield i, j


def spiral_indexes(
    start_index: np.array,
    corners: Tuple[int, int, int, int],
    max_radius: Optional[int] = None,
) -> Tuple[int, int]:
    radius = np.array([0, 0])
    min_y, max_y, min_x, max_x = corners
    stop_condition = False
    if max_radius is None:
        max_radius = np.inf
    while not stop_condition and radius[0] <= max_radius and radius[1] <= max_radius:
        bottom, left = start_index - radius
        top, right = start_index + radius
        do_bottom = True
        do_top = True
        do_left = True
        do_right = True
        if bottom < min_y and left < min_x and top > max_y and right > max_x:
            stop_condition = True
        if left < min_x:
            left = min_x
            do_left = False
        if top > max_y:
            top = max_y
            do_top = False
        if right > max_x:
            right = max_x
            do_right = False
        if bottom < min_y:
            bottom = min_y
            do_bottom = False

        if do_bottom:
            insert_index = bottom, left
            while insert_index[1] <= right:
                yield insert_index
                insert_index = insert_index[0], insert_index[1] + 1

        if do_right:
            insert_index = bottom, right
            while insert_index[0] <= top:
                yield insert_index
                insert_index = insert_index[0] + 1, insert_index[1]

        if do_top:
            insert_index = top, right
            while insert_index[1] >= left:
                yield insert_index
                insert_index = insert_index[0], insert_index[1] - 1

        if do_left:
            insert_index = top, left
            while insert_index[0] >= bottom:
                yield insert_index
                insert_index = insert_index[0] - 1, insert_index[1]

        radius += 1
