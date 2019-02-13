""" Implements the main functions used to solve the puzzle. """

from src.tan_network import TanNetwork


def format_output(path):
    """ 
    :parameter  path:   Path solving the puzzle
    :type       path:   List of TanStop instances

    :return:    Output formated as expected by the puzzle
    :rtype:     String
    """
    if not path:
        return "IMPOSSIBLE"
    else:
        return "\n".join([stop.name for stop in path])


def solve_puzzle(start, goal, stops, routes):
    """
    Encapsulates the logic used to solve the puzzle.
    This function directly takes the puzzle's inputs as arguments, and outputs the solution with the expected format.

    Such encapsulation allows to conveniently perform functional tests.
    """
    tan_network = TanNetwork(stops, routes)
    path = tan_network.get_shortest_path(start, goal)
    return format_output(path)
