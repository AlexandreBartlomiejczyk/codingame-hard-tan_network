""" Implements the logic related to the puzzle's context. """

import math
import re

from src.graph import DirectedEdge, DirectedGraph


EARTH_RADIUS_KM = 6371


class TanNetwork(DirectedGraph):
    """
    Represents the transportation network described in the puzzle.
    Since this network routes are stated to be directed, it is represented as a directed graph.
    """

    def __init__(self, stops_descriptions, routes_descriptions):
        """
        :parameter  stops_descriptions:   Descriptions of the stops as given by the puzzle's input
        :type       stops_descriptions:   List of strings

        :parameter  routes_descriptions:   Descriptions of the routes as given by the puzzle's input
        :type       routes_descriptions:   List of strings
        """
        stops = [TanStop(string) for string in stops_descriptions]
        self._stop_id_map = {stop.id: stop for stop in stops}

        routes = [self.get_route_from_string(route_string)
                  for route_string in routes_descriptions]

        super(TanNetwork, self).__init__(routes)

    def get_route_from_string(self, route_description):
        """
        :parameter  route_description:   Description of a route as given by the puzzle's input
        :type       route_description:   String

        :return:    Corresponding route object, used within this instance
        :rtype:     DirectedEdge(TanStop, TanStop)    
        """
        route_stop_strings = route_description.split()
        stop_start = self.get_stop_from_string(route_stop_strings[0])
        stop_end = self.get_stop_from_string(route_stop_strings[1])
        
        return DirectedEdge(stop_start, stop_end)

    def get_stop_from_string(self, stop_description):
        """
        :parameter  stop_description:   Description of a stop as given by the puzzle's input
        :type       stop_description:   String

        :return:    Corresponding stop object, used within this instance
        :rtype:     TanStop
        """
        stop_id = TanStop.extract_field_value('id', stop_description)
        return self.get_stop_from_id(stop_id)

    def get_stop_from_id(self, stop_id):
        """
        :parameter  stop_id:    The unique identifier of a stop
        :type       stop_id:    String

        :return:    Corresponding stop object, used within this instance
        :rtype:     TanStop
        """
        return self._stop_id_map[stop_id]

    def get_shortest_path(self, start_stop_description, goal_stop_description):
        """
        :parameter  start_stop_description:  Description of the stop to start from, as given by the puzzle's input
        :type       start_stop_description:  String

        :parameter  goal_stop_description:   Description of the stop to reach, as given by the puzzle's input
        :type       goal_stop_description:   String

        :return:    Shortest path between both given stops. Empty list if there is no valid path.
        :rtype:     List of TanStop
        """
        start_stop = self.get_stop_from_string(start_stop_description)
        goal_stop = self.get_stop_from_string(goal_stop_description)

        return super(TanNetwork, self).get_shortest_path_a_star(start_stop, goal_stop, self.get_distance)

    @staticmethod
    def get_distance(stop_1, stop_2):
        """ 
        Compute the distance between two stops, using to the puzzle's formula.

        :type   stop_1, stop2:  TanStop
        """
        x = (stop_2.longitude - stop_1.longitude) * math.cos((stop_1.latitude + stop_2.latitude)/2)
        y = stop_2.latitude - stop_1.latitude

        return math.sqrt(x*x + y*y) * EARTH_RADIUS_KM


class TanStop:
    """ Represents a stop of the transportation network described in the puzzle. """

    _fields_csv_indices = {'id':       0,
                           'name':     1,
                           'latitude':  3,
                           'longitude': 4}

    def __init__(self, input_string):
        """
        :parameter  input_string:   Description of a stop as given by the puzzle's input
        :type       input_string:   String
        """
        fields = input_string.split(',')

        for field, csv_index in self._fields_csv_indices.items():
            field_string = fields[csv_index]
            field_value = self.extract_field_value(field, field_string)

            self.__setattr__(field, field_value)

    def __str__(self):
        return self.name

    def __lt__(self, other):  # Arbitrary; only used for priority queues in case of priority tie
        return self.id < other.id

    @staticmethod
    def extract_field_value(field, field_string):
        """
        Extract the value of a stop field described in the puzzle from its associated encoded string.
        :parameter  field:  ('id' | 'name' | 'latitude' | 'longitude')
        """
        return getattr(TanStop, "_extract_" + field + "_value")(field_string)

    @staticmethod
    def _extract_id_value(string):
        stop_id_re = re.compile('StopArea\:([^ ]+)')
        id_match = stop_id_re.match(string)
        return id_match.groups()[0]

    @staticmethod
    def _extract_name_value(string):
        return string.strip('"')

    @staticmethod
    def _extract_latitude_value(string):
        return float(string)

    @staticmethod
    def _extract_longitude_value(string):
        return float(string)
