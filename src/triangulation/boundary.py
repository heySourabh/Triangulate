# Created on: May 9, 2023
# Author    : Sourabh Bhat <https://spbhat.in>

from triangulation.edge import Edge


class Boundary:
    def __init__(self, ref: int, edges: list[Edge]) -> None:
        self.ref = ref
        self.edges = edges
