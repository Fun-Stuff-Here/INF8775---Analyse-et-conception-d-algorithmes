import numpy as np
import copy
from encloser import Encloser
from direction import Direction
from typing import Optional, List, Tuple

class TreeNode:
    pass

class TreeNode:
    def __init__(self, encloser:Encloser, children:List[TreeNode], parent:Optional[TreeNode]) -> None:
        self.encloser :Encloser = encloser
        self.children :list[TreeNode] = children
        self.parent :Optional[TreeNode] = parent
        self.position : np.array = np.array([0, 0])

    def fill_children(self, zoo:np.array, direction: Direction) -> np.array:

        n_child = len(self.children)
        zoo_filled = self.fill(zoo, direction)

        if n_child == 0:
            return zoo

        buckets_of_children = self.split_children()
        directions = self.children_directions(direction)
        for children, child_direction in zip(buckets_of_children, directions):
            for child in children:
                child.fill_children(zoo_filled, child_direction)

        return zoo_filled

    def fill(self, zoo:np.array, direction: Direction)-> np.array:
        position = np.array([0,0]) if self.parent is None else self.parent.position
        while zoo[position] != -1:
            position += direction
        zoo[position] = self.encloser.encloser_number
        self.position = position
        return zoo

    def split_children(self) -> List[List[TreeNode]]:
        n_child = len(self.children)
        if n_child == 0:
            return []
        n_buckets = 4 if self.parent is None else 3

        buckets = [list()] * n_buckets
        
        for i, child in enumerate(self.children):
            buckets[i%n_buckets].append(child)

        return buckets

    def children_directions(self, direction:Direction)-> List[Direction]:
        directions = copy.deepcopy(Direction.VALUES)
        if self.parent is None:
            return directions

        directions.remove(direction.reverse())
        return directions

