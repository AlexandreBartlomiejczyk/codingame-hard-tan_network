from src.main import solve_puzzle
from utils_ut import TestCaseAAA


class TestFunctionnality(TestCaseAAA):
    """
    Ensures the proper functionality of the solution.
    This test case is based on the result example given in the puzzle's description.
    """
    def _arrange(self, start_id_input, goal_id_input, stops_input, routes_input):
        self._start_id_input = start_id_input
        self._goal_id_input = goal_id_input
        self._stops_input = stops_input
        self._routes_input = routes_input

    def _act(self):
        self._result = solve_puzzle(self._start_id_input,
                                    self._goal_id_input,
                                    self._stops_input,
                                    self._routes_input)

    def _assert(self, expected_output):
        self.assertEqual(self._result, expected_output)

    def test_example(self):
        self._arrange(start_id_input="StopArea:ABDU",
                      goal_id_input="StopArea:ABLA",
                      stops_input=['StopArea:ABDU,"Abel Durand",,47.22019661,-1.60337553,,,1,',
                                   'StopArea:ABLA,"Avenue Blanche",,47.22973509,-1.58937990,,,1,',
                                   'StopArea:ACHA,"Angle Chaillou",,47.26979248,-1.57206627,,,1,'],
                      routes_input=["StopArea:ABDU StopArea:ABLA",
                                    "StopArea:ABLA StopArea:ACHA"])
        self._act()
        self._assert(expected_output="Abel Durand\nAvenue Blanche")
