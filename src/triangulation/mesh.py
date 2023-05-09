# Created on: May 9, 2023
# Author    : Sourabh Bhat <https://spbhat.in>

from triangulation.boundary import Boundary
from triangulation.node import Node
from triangulation.triangle import Triangle


class Mesh:
    def __init__(self) -> None:
        self.nodes: list[Node] = []
        self.triangles: list[Triangle] = []
        self.boundaries: list[Boundary] = []
