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


def draw_triangle(triangle: Triangle, show_edges=True,
                  show_nodes=False, show_circumcircle=False):
    n1 = triangle.node1.point
    n2 = triangle.node2.point
    n3 = triangle.node3.point

    if show_edges:
        nodes = np.array([n1, n2, n3, n1])
        plt.plot(nodes[:, 0], nodes[:, 1], lw=1, color="black")

    if show_nodes:
        nodes = np.array([n1, n2, n3])
        plt.plot(nodes[:, 0], nodes[:, 1], "o", color="blue")

    if show_circumcircle:
        circle = triangle.circumcircle
        theta = np.linspace(0, 2*np.pi, 500)
        c = circle.center
        r = circle.radius
        x, y = r * np.array([np.cos(theta), np.sin(theta)])
        plt.plot(x + c.x, y + c.y, "--", lw=1, color="green")

        # cross-hair
        ch_size = r * 0.05
        ch_xy = np.array([-ch_size, ch_size])
        plt.plot(c.x + ch_xy, [c.y, c.y], "-", lw=1, color="black")
        plt.plot([c.x, c.x], c.y + ch_xy, "-", lw=1, color="black")

    clicked_triangle = None

    def highlight_triangle(point):
        nonlocal clicked_triangle
        if not triangle.contains_point(point):
            return
        nodes = np.array([n1, n2, n3])
        clicked_triangle = plt.fill(nodes[:, 0], nodes[:, 1], color=(1, 0, 0, 0.5))

    def unhighlight_triangle():
        nonlocal clicked_triangle
        if clicked_triangle != None:
            for t in clicked_triangle:
                t.remove()
            clicked_triangle = None

    clicked_circumcircle = None

    def highlight_circumcircle(point):
        nonlocal clicked_circumcircle
        if not triangle.contains_point(point):
            return
        circle = triangle.circumcircle
        theta = np.linspace(0, 2*np.pi, 500)
        c = circle.center
        r = circle.radius
        x, y = r * np.array([np.cos(theta), np.sin(theta)])
        clicked_circumcircle = plt.plot(x + c.x, y + c.y, "--", lw=0.75, color="red")

    def unhighlight_circumcircle():
        nonlocal clicked_circumcircle
        if clicked_circumcircle != None:
            for c in clicked_circumcircle:
                c.remove()
            clicked_circumcircle = None

    clicked_point = None

    def on_click(event):
        nonlocal clicked_point
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata
        if x == None or y == None:
            if clicked_point != None:
                clicked_point.remove()
                clicked_point = None
            unhighlight_triangle()
            unhighlight_circumcircle()
            plt.draw()
            return
        point = Point(x, y)
        if clicked_point != None:
            clicked_point.remove()
        if clicked_triangle != None:
            unhighlight_triangle()
        if clicked_circumcircle != None:
            unhighlight_circumcircle()

        clicked_point = plt.scatter([x,], [y,], color="red")
        highlight_triangle(point)
        highlight_circumcircle(point)

        plt.draw()

    plt.gcf().canvas.mpl_connect('button_press_event', on_click)


if __name__ == "__main__":
    test_triangle()
