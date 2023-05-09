# Created on: May 9, 2023
# Author    : Sourabh Bhat <https://spbhat.in>

import unittest
from typing import Union

import numpy as np
from geom.point import Point
from triangulation.node import Node


class NodeSearchTree:
    def __init__(self) -> None:
        self._root: Union[None, "Cell"] = None

    def add_node(self, node: Node):
        if self._root == None:
            self._root = Cell(node)
            return

        self._root.add_node(node)

    def search_node(self, point: Point) -> Node:
        if self._root == None:
            raise RuntimeError(
                "Node not added yet. Please add nodes before searching.")

        pt_array = np.array([point.x, point.y])
        return self._root.search(pt_array).node


overlap_eps = 1e-12


class Split:
    def __init__(self, direction: int, location: float) -> None:
        self.direction = direction
        self.location = location


class Children:
    def __init__(self, left: "Cell", right: "Cell", split: Split) -> None:
        self.left = left
        self.right = right
        self.split = split


class Cell:
    def __init__(self, node: Node) -> None:
        self.node: Node = node
        self.children: Union[Children, None] = None

    def add_node(self, node: Node) -> None:
        if self.children == None:
            p1 = node.point
            p2 = self.node.point
            distance = np.abs(p1 - p2)
            if np.sum(distance**2) < overlap_eps:
                raise ValueError("Overlapping / almost overlapping points.")
            split_direction = int(np.argmax(distance))
            split_location = (p1[split_direction] + p2[split_direction]) / 2
            split = Split(split_direction, split_location)
            if p1[split_direction] < split_location:
                left = Cell(node)
                right = Cell(self.node)
            else:
                left = Cell(self.node)
                right = Cell(node)
            self.children = Children(left, right, split)
        else:
            split = self.children.split
            split_direction = split.direction
            split_location = split.location
            if node.point[split_direction] < split_location:
                self.children.left.add_node(node)
            else:
                self.children.right.add_node(node)

    def search(self, point: np.ndarray) -> "Cell":
        if self.children == None:
            return self
        else:
            split = self.children.split
            split_direction = split.direction
            split_location = split.location
            if point[split_direction] < split_location:
                return self.children.left.search(point)
            else:
                return self.children.right.search(point)


class TestNodeSearch(unittest.TestCase):

    def test_raises_error_if_searching_empty_tree(self):
        tree = NodeSearchTree()
        with self.assertRaises(RuntimeError):
            tree.search_node(Point(1, 1))

    def test_search(self):
        tree = NodeSearchTree()
        node1 = Node(0, Point(1, 1))
        tree.add_node(node1)

        self.assertEquals(tree.search_node(Point(0, 1)), node1)

        node2 = Node(1, Point(0, 0))
        tree.add_node(node2)

        self.assertEquals(tree.search_node(Point(0.51, 0.51)), node1)
        self.assertEquals(tree.search_node(Point(0.49, 0.49)), node2)

        self.assertEquals(tree.search_node(Point(1.1, 1.5)), node1)
        self.assertEquals(tree.search_node(Point(0.1, -5)), node2)


if __name__ == "__main__":
    unittest.main()
