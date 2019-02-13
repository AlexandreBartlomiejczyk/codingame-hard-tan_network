""" Implements utility classes and functions for unit tests. """

from unittest import TestCase


class TestCaseAAA(TestCase):
    """ This class is a template for unit tests, whose structure follow the 'Arrange - Act - Assert' principle. """

    def _arrange(self):
        raise NotImplementedError

    def _act(self):
        raise NotImplementedError

    def _assert(self):
        raise NotImplementedError
