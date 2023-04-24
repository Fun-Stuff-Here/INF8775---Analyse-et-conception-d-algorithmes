import numpy as np
import copy
import random
from encloser import Encloser
from direction import Direction
from typing import Optional, List


class TreeNode:
    pass


class TreeNode:
    def __init__(
        self,
        encloser: Encloser,
        children: List[TreeNode],
        parent: Optional[TreeNode],
    ) -> None:
        self.encloser: Encloser = encloser
        self.children: list[TreeNode] = children
        self.parent: Optional[TreeNode] = parent
        self.position: np.array = np.array([])

    def fill_children(self, zoo: np.array, direction: Direction) -> np.array:
        n_child = len(self.children)
        zoo_filled = self.fill(zoo, direction)

        if n_child == 0:
            return zoo

        directions = self.children_directions(direction)
        buckets_of_children = self.split_children(len(directions))
        for children, child_direction in zip(buckets_of_children, directions):
            for child in children:
                child.fill_children(zoo_filled, child_direction)

        return zoo_filled

    def fill(self, zoo: np.array, direction: Direction) -> np.array:
        position = (
            np.array([zoo.shape[0] // 2, zoo.shape[1] // 2])
            if self.parent is None
            else copy.deepcopy(self.parent.position)
        )

        while zoo[position[0], position[1]] != -1:
            position += direction
        zoo[position[0], position[1]] = self.encloser.encloser_number
        self.position = position

        return zoo

    def split_children(self, n_buckets: int) -> List[List[TreeNode]]:
        n_child = len(self.children)
        if n_child == 0:
            return []

        buckets = [list() for _ in range(n_buckets)]
        for i, child in enumerate(self.children):
            buckets[i % n_buckets].append(child)

        return buckets

    def children_directions(self, direction: Direction) -> List[Direction]:
        directions = copy.deepcopy(Direction.VALUES)
        random.shuffle(directions)
        if self.parent is None:
            return directions

        for i, a_direction in enumerate(directions):
            if a_direction[0] == direction[0] and a_direction[1] == direction[1]:
                directions.pop(i)
                break

        return directions
