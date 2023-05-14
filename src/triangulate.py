# Created on: May 10, 2023
# Author    : Sourabh Bhat <https://spbhat.in>

from matplotlib import pyplot as plt
import numpy as np
from geom.point import Point
from draw import draw_triangle
from triangulation.edge import Edge
from triangulation.node import Node
from triangulation.node_search import NodeSearchTree
from triangulation.triangle import Triangle

overlap_eps = 1e-12

# TODO: 1. Generate mesh for given outer boundaries and inner boundaries (holes)
#       2. Constrained Delaunay to preserve the boundaries
#       3. Group boundary edges with same tag/ref
#       4. Mesh quality control using given criteria / solution / metric
#       5. Further optimize triangulation using directional search method


def search_triangle(point: Point, nearby_node: Node) -> Triangle:
    # TODO: Optimize using directional search
    already_searched_nodes = []
    nodes_to_search = [nearby_node, ]

    for node in nodes_to_search:
        if node in already_searched_nodes:
            continue
        for tri in node.nbrs:
            if tri.contains_point(point):
                return tri
            nodes_to_search.append(tri.node1)
            nodes_to_search.append(tri.node2)
            nodes_to_search.append(tri.node3)
        already_searched_nodes.append(node)

    raise ValueError("New point is inserted outside existing triangulation.")


class Triangulation:
    def __init__(self, super_triangle: Triangle) -> None:
        n1 = super_triangle.node1
        n2 = super_triangle.node2
        n3 = super_triangle.node3

        self.nodes = [n1, n2, n3]

        self.tree = NodeSearchTree()
        self.tree.add_node(n1)
        self.tree.add_node(n2)
        self.tree.add_node(n3)

        self.node_index = 0
        self.super_triangle_removed = False

    def insert_node(self, x: float, y: float):
        new_point = Point(x, y)
        # Search the node closest to (x,y) from the tree
        nearby_node = self.tree.search_node(new_point)

        # Search the triangle containing (x,y) from node.nbrs
        center_triangle = search_triangle(new_point, nearby_node)

        # Set of triangles in vicinity ( = set of nbrs of three nodes of the triangle containing (x,y))
        nearby_triangles: set[Triangle] = set()
        n1 = center_triangle.node1
        n2 = center_triangle.node2
        n3 = center_triangle.node3
        nearby_triangles.update(n1.nbrs)
        nearby_triangles.update(n2.nbrs)
        nearby_triangles.update(n3.nbrs)
        checked_nodes = [n1, n2, n3]
        level2_triangles = []
        for tri in nearby_triangles:
            nodes = [tri.node1, tri.node2, tri.node3]
            for n in nodes:
                if n not in checked_nodes:
                    level2_triangles.extend(n.nbrs)
                    checked_nodes.append(n)
        nearby_triangles.update(level2_triangles)

        # Mark bad triangles ( = triangles whose circumcircle contains (x,y))
        bad_triangles: list[Triangle] = []
        for tri in nearby_triangles:
            if tri.circumcircle.contains_point(new_point):
                bad_triangles.append(tri)

        # List of edges which do not share bad triangles (polygon of hole)
        hole_edges: list[Edge] = []
        for tri in bad_triangles:
            tri_edges = [Edge(tri.node1, tri.node2),
                         Edge(tri.node2, tri.node3),
                         Edge(tri.node3, tri.node1)]
            for e in tri_edges:
                if e in hole_edges:
                    hole_edges.remove(e)
                else:
                    hole_edges.append(e)

        # Remove bad triangles
        for tri in bad_triangles:
            tri.remove()

        # Create new triangles using edges of the polygon & Node(x,y)
        new_node = Node(self.node_index, new_point)
        self.node_index += 1
        for e in hole_edges:
            Triangle(new_node, e.node1, e.node2)

        # insert new node in tree
        self.nodes.append(new_node)
        self.tree.add_node(new_node)

    def remove_super_triangle(self):
        if self.super_triangle_removed:
            return

        super_nodes = self.nodes[:3]
        for n in super_nodes:
            nbrs = n.nbrs.copy()
            for tri in nbrs:
                tri.remove()
        self.nodes = self.nodes[3:]

        self.super_triangle_removed = True

    def get_triangulation(self) -> tuple[list[Node], set[Triangle]]:
        self.remove_super_triangle()
        triangles: set[Triangle] = set()

        for node in self.nodes:
            triangles.update(node.nbrs)

        return (self.nodes, triangles)


def main(num_nodes):
    seed = np.random.randint(0, 10000)
    print(f"Random seed = {seed}")
    np.random.seed(seed)
    # points = [Point(0, 0), Point(0.4, 0), Point(0.4, 0.2), Point(1, 0.2), Point(1, 0.5), Point(0, 0.5)]
    points = [Point(np.random.uniform(10, 20), np.random.uniform(-2, 5)) for _ in range(num_nodes)]

    x, y = np.array([(p.x, p.y) for p in points]).T
    minx = np.min(x)
    maxx = np.max(x)
    miny = np.min(y)
    maxy = np.max(y)

    max_dx = maxx - minx
    max_dy = maxy - miny
    if max_dx < overlap_eps or max_dy < overlap_eps:
        raise ValueError("Cannot triangulate collinear points.")

    scale = 2 / max(max_dx, max_dy)
    shiftx = (minx + maxx) / 2
    shifty = (miny + maxy) / 2

    xs, ys = (x - shiftx) * scale, (y - shifty) * scale

    # Super triangle
    node1 = Node(-1, Point(0, 50))
    node2 = Node(-2, Point(-50, -30))
    node3 = Node(-3, Point(50, -30))
    super_triangle = Triangle(node1, node2, node3)

    triangulation = Triangulation(super_triangle)
    for px, py in zip(xs, ys):
        triangulation.insert_node(px, py)
    nodes, triangles = triangulation.get_triangulation()
    print(f"Nodes={len(nodes)}, Triangles={len(triangles)}")

    print("Triangulation Done.")
    print("Showing Triangulation...")

    # Scale back to original location
    for n in nodes:
        n.point = n.point / scale + np.array([shiftx, shifty])
    for tri in triangles:
        tri.update_circumcircle_and_area()

    nodes_x, nodes_y = np.array([n.point for n in nodes]).T
    plt.figure("Triangulation: Programmed by Sourabh Bhat")
    plt.cla()
    plt.plot(nodes_x, nodes_y, "o")

    for tri in triangles:
        draw_triangle(tri, show_circumcircle=False)

    plt.gca().set_aspect("equal")
    plt.title("Click to highlight triangle and circumcircle")
    plt.xlim(np.array([minx, maxx]) + 0.05 * np.array([-1, 1]) * max_dx)
    plt.ylim(np.array([miny, maxy]) + 0.05 * np.array([-1, 1]) * max_dy)
    # plt.xticks([])
    # plt.yticks([])
    # plt.tight_layout()
    # plt.savefig(f"mesh_{num_nodes:03d}")
    plt.show()


if __name__ == "__main__":
    main(30)
