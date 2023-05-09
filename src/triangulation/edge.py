# Created on: May 9, 2023
# Author    : Sourabh Bhat <https://spbhat.in>

from triangulation.node import Node


class Edge:
    def __init__(self, node1: Node, node2: Node) -> None:
        self.node1 = node1
        self.node2 = node2
