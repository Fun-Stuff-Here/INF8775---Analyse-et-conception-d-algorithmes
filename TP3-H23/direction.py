import numpy as np


class Direction:
    pass


class Direction:
    NORTH = np.array([0, 1])
    NORTH_WEST = np.array([-1, 1])
    NORTH_EAST = np.array([1, 1])
    WEST = np.array([-1, 0])
    EAST = np.array([1, 0])
    SOUTH = np.array([0, -1])
    SOUTH_WEST = np.array([-1, -1])
    SOUTH_EAST = np.array([1, -1])

    VALUES = [
        NORTH,
        NORTH_WEST,
        NORTH_EAST,
        WEST,
        EAST,
        SOUTH,
        SOUTH_WEST,
        SOUTH_EAST,
    ]
