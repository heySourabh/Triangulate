# Created on: May 8, 2023
# Author    : Sourabh Bhat <https://spbhat.in>

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
