""" Implements the logic related to graph theory. """

import math
from collections import namedtuple

from src.utils import PriorityQueue


DirectedEdge = namedtuple('DirectedEdge', ['start', 'end'])


class DirectedGraph:
    """
    Represents a directed graph.
    Provides a shortest path calculation method (relying on the A* algorithm).

    This is an abstract class, as some operations associated with graphs are related to distances between vertices,
    which are problem-specific.
    """

    class AStarData:
        """
        Convenience class used to contain the data needed by the A* algorithm, and perform the data operations
        associated with the main steps of the latter.
        """
        def __init__(self, vertices, start_vertex):
            self._cost_to = {vertex: math.inf for vertex in vertices}
            self._cost_to[start_vertex] = 0

            self._priority_queue = PriorityQueue()
            self._priority_queue.push(0, start_vertex)

            self._current_vertex = None
            self._already_visited_vertices = set()
            self._path_trace = {}

        @property
        def current_vertex(self):
            # the current vertex should only be set by the visit_next_vertex method, hence the usage of this property
            return self._current_vertex

        def visit_next_vertex(self):
            next_vertex = self._priority_queue.pop()
            self._current_vertex = next_vertex
            self._already_visited_vertices.add(next_vertex)

        def get_cost_to(self, vertex):
            return self._cost_to[vertex]

        def register_neighbor(self, neighbor, cost_to_neighbor, estimated_cost_via_neighbor):
            self._path_trace[neighbor] = self.current_vertex
            self._cost_to[neighbor] = cost_to_neighbor
            self._priority_queue.push(estimated_cost_via_neighbor, neighbor)

        def reconstruct_path_to(self, vertex):
            current = vertex
            path = [vertex]

            while current in self._path_trace.keys():
                current = self._path_trace[current]
                path.insert(0, current)

            return path

        def has_already_visited(self, vertex):
            return vertex in self._already_visited_vertices

        def has_vertices_to_visit(self):
            return not self._priority_queue.is_empty()

    def __init__(self, edges):
        """
        :parameter  edges:  Edges composing the graph
        :type       edges:  Iterable of DirectedEdge
        """
        self.representation = {}

        for edge in edges:
            self.add_edge(edge)

    def add_edge(self, edge):
        """
        :parameter  edge:   Edge to add to the graph's representation
        :type       edge:   DirectedEdge
        """
        try:
            self.representation[edge.start].add(edge.end)
        except KeyError:
            self.representation[edge.start] = set([edge.end])

        self.representation.setdefault(edge.end, set())

    def get_shortest_path_a_star(self, start_vertex, goal_vertex, cost_heuristic):
        """
        Compute the shortest path between two points, using the A* algorithm.

        :parameter  start_vertex:   Vertex to start from  
        :parameter  goal_vertex:    Vertex to reach

        :parameter  cost_heuristic: Function estimating the cost to get from one vertex to another.
                                    Also refered to as 'heuristic', or 'h(n)' in the literature of graph theory related
                                    to A*.
        :type       cost_heuristic: Function with the following signature: f(vertex_1, vertex_2)

        :return:    Shortest path between both given vertices. Empty list if there is no valid path
        """
        a_star = DirectedGraph.AStarData(self.vertices, start_vertex)

        while a_star.has_vertices_to_visit():
            a_star.visit_next_vertex()

            if a_star.current_vertex == goal_vertex:
                return a_star.reconstruct_path_to(a_star.current_vertex)

            for neighbor in self.representation[a_star.current_vertex]:
                if a_star.has_already_visited(neighbor):
                    continue

                cost_to_neighbor = a_star.get_cost_to(a_star.current_vertex) +\
                                   self.get_distance(a_star.current_vertex, neighbor)
                estimated_cost_via_neighbor = cost_to_neighbor + cost_heuristic(neighbor, goal_vertex)

                a_star.register_neighbor(neighbor, cost_to_neighbor, estimated_cost_via_neighbor)

        return []

    @property
    def vertices(self):
        """ :return: Vertices composing the graph """
        return self.representation.keys()

    @staticmethod
    def get_distance(vertex_1, vertex_2):
        """ :return: Distance between the two given vertices """
        raise NotImplementedError
