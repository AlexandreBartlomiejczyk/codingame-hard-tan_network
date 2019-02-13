""" Implements utility classes and functions. """

from heapq import heappop, heappush


class PriorityQueue:
    """ Implements a basic priority queue. """

    def __init__(self):
        self._queue = []
        self._counter = 0  # Used to choose an element in case of a priority tie

    def push(self, priority, element):
        heappush(self._queue, (priority, self._counter, element))
        self._counter += 1

    def pop(self):
        return heappop(self._queue)[2]

    def is_empty(self):
        return not self._queue
