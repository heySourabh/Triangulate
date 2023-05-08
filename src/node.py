# Created on: May 8, 2023
# Author    : Sourabh Bhat <https://spbhat.in>

import numpy as np
from point import Point


class Node:
    def __init__(self, index: int, point: Point) -> None:
        self.index = index
        self.point = np.array([point.x, point.y])
