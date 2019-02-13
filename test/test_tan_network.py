from src.tan_network import TanStop
from utils_ut import TestCaseAAA


class TestTanStop_Init(TestCaseAAA):
    """
    Ensures proper initialization of TanStop instances.
    All the tests are based on the stop description examples given in the puzzle's description.
    """

    def _arrange(self, input_string):
        self._input_string = input_string

    def _act(self):
        self._uut = TanStop(self._input_string)

    def _assert(self, expected_attributes):
        uut_attributes = vars(self._uut)

        for attribute_key, expected_value in expected_attributes.items():
            self.assertEqual(uut_attributes[attribute_key], expected_value)

    def test_stop_example_1(self):
        self._arrange(input_string='StopArea:ABDU,"Abel Durand",,47.22019661,-1.60337553,,,1,')
        self._act()
        self._assert(expected_attributes={'id': 'ABDU',
                                          'name': 'Abel Durand',
                                          'latitude': 47.22019661,
                                          'longitude': -1.60337553})

    def test_stop_example_2(self):
        self._arrange(input_string='StopArea:ABLA,"Avenue Blanche",,47.22973509,-1.58937990,,,1,')
        self._act()
        self._assert(expected_attributes={'id': 'ABLA',
                                          'name': 'Avenue Blanche',
                                          'latitude': 47.22973509,
                                          'longitude': -1.58937990})

    def test_stop_example_3(self):
        self._arrange(input_string='StopArea:ACHA,"Angle Chaillou",,47.26979248,-1.57206627,,,1,')
        self._act()
        self._assert(expected_attributes={'id': 'ACHA',
                                          'name': 'Angle Chaillou',
                                          'latitude': 47.26979248,
                                          'longitude': -1.57206627})
