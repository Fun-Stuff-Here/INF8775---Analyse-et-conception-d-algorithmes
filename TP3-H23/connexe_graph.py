import numpy as np
from encloser import Encloser
from typing import Optional, Tuple
from direction import Direction
from indexes import neighbor_indexes


class ConnexeGraph:
    def __init__(
        self,
        zoo: np.array,
        encloser: Encloser,
        index: Tuple[int, int],
        zoo_corners: Tuple[int, int, int, int],
    ):
        self.zoo: np.array = zoo
        self.connexe: Optional[bool] = False
        self.visited: np.array = np.zeros_like(self.zoo, dtype=bool) * False
        self.queue: list = []
        self.encloser: Encloser = encloser
        self.start: Tuple[int, int] = index
        self.zoo_corners: Tuple[int, int, int, int] = zoo_corners

    def bfs(self):
        self.count: int = 1
        self.queue.append(self.start)
        self.visited[self.start] = True
        while self.queue:
            node = self.queue.pop(0)
            for neighbor in neighbor_indexes(node, self.zoo_corners):
                if (
                    self.zoo[neighbor] == self.encloser.encloser_number
                    and not self.visited[neighbor]
                ):
                    self.queue.append(neighbor)
                    self.count += 1
                    self.visited[neighbor] = True
        if self.count >= self.encloser.size:
            self.connexe = True

    def is_connexe(self) -> bool:
        self.bfs()
        return self.connexe
