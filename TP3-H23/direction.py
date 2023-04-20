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
        np.array([0, 1]),
        np.array([-1, 1]),
        np.array([1, 1]),
        np.array([-1, 0]),
        np.array([1, 0]),
        np.array([0, -1]),
        np.array([-1, -1]),
        np.array([1, -1]),
    ]

    def __init__(self, direction: np.array) -> None:
        self.vector = direction

    def reverse(self) -> Direction:
        return Direction(self.vector*-1)
    
