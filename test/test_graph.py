from unittest.mock import patch

from src.graph import DirectedEdge, DirectedGraph
from utils_ut import TestCaseAAA


class DummyVertex:
    def __init__(self, id_):
        self.id = id_

    def __str__(self):  # useful in debugger
        return self.id

A = DummyVertex("A")
B = DummyVertex("B")
C = DummyVertex("C")
D = DummyVertex("D")
E = DummyVertex("E")


def generate_directed_edges(edge_tuples):
    return [DirectedEdge(*edge_tuple) for edge_tuple in edge_tuples]


class TestDirectedGraph_Init(TestCaseAAA):
    """
    Ensures proper initialization of DirectGraph subclasses instances.
    Since only the calculation of the distance between two vertices requires to subclass DirectedGraph, and such
    calculation is not needed as part of this test case, DirectGraph is directly instantiated here.
    """

    def _arrange(self, edge_tuples):
        self._edges = generate_directed_edges(edge_tuples)

    def _act(self):
        self._uut = DirectedGraph(self._edges)

    def _assert(self, expected_representation):
        self.assertEqual(self._uut.representation, expected_representation)

    def test_empty(self):
        self._arrange(edge_tuples=[])
        self._act()
        self._assert(expected_representation={})

    def test_one_edge(self):
        self._arrange(edge_tuples=[(A, B)])
        self._act()
        self._assert(expected_representation={A: set([B]),
                                              B: set()})
    
    # graph with bidirected edges only
    def test_symmetric(self):
        self._arrange(edge_tuples=[(A, B),  
                                   (A, C),
                                   (B, A),
                                   (C, A)])
        self._act()
        self._assert(expected_representation={A: set([B, C]),
                                              B: set([A]),
                                              C: set([A])})

    # graph with no bidirected edges
    def test_oriented(self):
        self._arrange(edge_tuples=[(A, B),  
                                   (A, C)])
        self._act()
        self._assert(expected_representation={A: set([B, C]),
                                              B: set(),
                                              C: set()})

    # graph with bidirected and simple directed edges
    def test_mixed(self):
        self._arrange(edge_tuples=[(A, B),  
                                   (A, C),
                                   (B, A)])
        self._act()
        self._assert(expected_representation={A: set([B, C]),
                                              B: set([A]),
                                              C: set()})

    def test_closed(self):
        self._arrange(edge_tuples=[(A, B),  
                                   (A, C),
                                   (B, A),
                                   (C, B)])
        self._act()
        self._assert(expected_representation={A: set([B, C]),
                                              B: set([A]),
                                              C: set([B])})


class TestDirectedGraph_AStar(TestCaseAAA):
    """
    Tests the A* implementation's results, while using:
    - a null heuristic (resulting in a behavior similar to Dijkstra's algorithm)
    - an exact heuristic (which is the upper limit for the algorithm to remain valid)

    Does however not evaluate the heuristic's influence on the vertices selection.
    """

    def setUp(self):
        edges = generate_directed_edges([(A, B), (E, B),
                                         (A, C), (C, A), (C, E),
                                         (A, D), (D, A), (D, E), (E, D)])
        self._uut = DirectedGraph(edges)
        self._start = None
        self._goal = None

        self._distances = {frozenset([A, E]): 3,  # frozensets are hashable while regular sets are not; only the former
                                                  # can therefore be used as dictionaries keys

                           frozenset([B, A]): 2,
                           frozenset([B, E]): 2,

                           frozenset([C, A]): 2.5,
                           frozenset([C, E]): 2.5,

                           frozenset([D, A]): 1,
                           frozenset([D, E]): 5}

    def _get_distance_mock(self, vertex_1, vertex_2):
        try:
            distance = self._distances[frozenset([vertex_1, vertex_2])]
        except KeyError:  # Case of an irrelevant distance
            distance = 0

        return distance

    def _arrange(self, start, goal):
        self._start = start
        self._goal = goal

    def _act(self):
        with patch.object(self._uut, 'get_distance', side_effect=self._get_distance_mock):
            self._result_no_heuristic = self._uut.get_shortest_path_a_star(self._start, self._goal, lambda *args: 0)
            self._result_exact_heuristic = self._uut.get_shortest_path_a_star(self._start, self._goal,
                                                                              self._get_distance_mock)

    def _assert(self, expected_path):
        self.assertEqual(self._result_no_heuristic, expected_path)
        self.assertEqual(self._result_exact_heuristic, expected_path)

    def test_no_path(self):
        self._arrange(start=B, goal=C)
        self._act()
        self._assert(expected_path=[])

    def test_one_edge_one_path(self):
        self._arrange(start=E, goal=B)
        self._act()
        self._assert(expected_path=[E, B])
    
    def test_one_edge_two_paths(self):
        self._arrange(start=C, goal=E)
        self._act()
        self._assert(expected_path=[C, E])

    def test_two_edges_one_path(self):
        self._arrange(start=E, goal=A)
        self._act()
        self._assert(expected_path=[E, D, A])

    def test_two_edges_two_paths(self):
        self._arrange(start=A, goal=E)
        self._act()
        self._assert(expected_path=[A, C, E])
