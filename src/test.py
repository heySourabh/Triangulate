#!/usr/bin/python3

# Created on: May 8, 2023
# Author    : Sourabh Bhat <https://spbhat.in>

import numpy as np
from matplotlib import pyplot as plt

from geom.point import Point
from triangulation.node import Node
from triangulation.triangle import Triangle


def test_triangle():
    p1 = Point(-7.1, 5.2)
    p2 = Point(1.5, 2.8)
    p3 = Point(-8.1, -1)
    t1 = Triangle(Node(0, p1), Node(1, p2), Node(2, p3))

    plt.xlabel("x")
    plt.ylabel("y")
    plt.gca().set_aspect("equal")
    draw_triangle(t1, show_nodes=True, show_circumcircle=True)

    plt.show()


def draw_triangle(triangle: Triangle, show_edges=True, show_nodes=False, show_circumcircle=False):
    n1 = triangle.node1.point
    n2 = triangle.node2.point
    n3 = triangle.node3.point

    if show_edges:
        nodes = np.array([n1, n2, n3, n1])
        plt.plot(nodes[:, 0], nodes[:, 1], lw=2, color="black")

    if show_nodes:
        nodes = np.array([n1, n2, n3])
        plt.plot(nodes[:, 0], nodes[:, 1], "o", color="blue")

    if show_circumcircle:
        circle = triangle.circumcircle
        theta = np.linspace(0, 2*np.pi, 100)
        c = circle.center
        r = circle.radius
        x, y = r * np.array([np.cos(theta), np.sin(theta)])
        plt.plot(x + c.x, y + c.y, "--", lw=1, color="green")

        # cross-hair
        ch_size = r * 0.05
        ch_xy = np.array([-ch_size, ch_size])
        plt.plot(c.x + ch_xy, [c.y, c.y], "-", lw=1, color="black")
        plt.plot([c.x, c.x], c.y + ch_xy, "-", lw=1, color="black")

    clicked_point = None

    def on_click(event):
        nonlocal clicked_point
        x, y = event.xdata, event.ydata
        if x == None or y == None:
            return
        point = Point(x, y)
        if clicked_point != None:
            clicked_point.remove()

        clicked_point = plt.scatter([x,], [y,], color="red")
        plt.draw()
        print(("Inside" if triangle.is_point_in_circumcircle(point) else "Outside") + " circumcircle,",
              ("Inside" if triangle.is_point_in_triangle(point) else "Outside") + " triangle")

    plt.gcf().canvas.mpl_connect('button_press_event', on_click)


if __name__ == "__main__":
    test_triangle()
