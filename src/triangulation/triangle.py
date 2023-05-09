# Created on: May 8, 2023
# Author    : Sourabh Bhat <https://spbhat.in>

import numpy as np

from geom.circle import Circle
from geom.point import Point
from triangulation.node import Node


class Triangle:
    def __init__(self, node1: Node, node2: Node, node3: Node) -> None:
        self.node1 = node1
        self.node2 = node2
        self.node3 = node3

        area = Triangle._area(node1.point, node2.point, node3.point)
        if area < 0:  # ensure counter-clockwise nodes
            self.node1 = node2
            self.node2 = node1

        self.area = np.abs(area)

        self.circumcircle: Circle = Triangle._circumcircle(
            node1.point, node2.point, node3.point)

    def is_point_in_circumcircle(self, point: Point) -> bool:
        circle = self.circumcircle
        c = circle.center
        r = circle.radius
        dx = point.x - c.x
        dy = point.y - c.y
        return dx*dx + dy*dy < r*r

    def is_point_in_triangle(self, point: Point) -> bool:
        p1 = self.node1.point
        p2 = self.node2.point
        p3 = self.node3.point

        s = (p1[1] * p3[0] - p1[0] * p3[1] + (p3[1] - p1[1])
             * point.x + (p1[0] - p3[0]) * point.y)
        t = (p1[0] * p2[1] - p1[1] * p2[0] + (p1[1] - p2[1])
             * point.x + (p2[0] - p1[0]) * point.y)

        return s > 0 and t > 0 and (s + t) < 2 * self.area

    @staticmethod
    def _circumcircle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> Circle:
        vab = b - a
        vac = c - a
        v1 = a + b
        v2 = a + c

        M = np.array([vab, vac])
        rhs = np.array([vab.dot(v1), vac.dot(v2)])
        xy = np.linalg.solve(M, rhs) / 2
        radius = np.sqrt(np.sum((a - xy)**2))

        return Circle(Point(xy[0], xy[1]), radius)

    @staticmethod
    def _area(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
        vab = b - a
        vac = c - a
        area = float(np.cross(vab, vac))
        return 0.5 * area