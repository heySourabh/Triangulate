# Created on: May 8, 2023
# Author    : Sourabh Bhat <https://spbhat.in>

from geom.point import Point


class Circle:
    def __init__(self, center: Point, radius: float) -> None:
        self.center = center
        self.radius = radius
