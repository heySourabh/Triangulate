# Created on: May 9, 2023
# Author    : Sourabh Bhat <https://spbhat.in>

from triangulation.node import Node


class Edge:
    def __init__(self, node1: Node, node2: Node) -> None:
        self.node1 = node1
        self.node2 = node2

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return False

        condition1 = (self.node1 == other.node1) and (self.node2 == other.node2)
        condition2 = (self.node1 == other.node2) and (self.node2 == other.node1)
        return condition1 or condition2
