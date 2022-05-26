from unittest import TestCase
from Automata import Automata

class TestAutomata(TestCase):
    def test_types(self):
        auto = Automata("AC", "ACA")
        self.assertRaises(TypeError, auto.check_pattern_alphabet, "phge")
        self.assertRaises(TypeError, auto.check_pattern_alphabet, True)
        self.assertRaises(TypeError, auto.check_pattern_alphabet, 1654)
        self.assertRaises(TypeError, auto.check_pattern_alphabet, "AC", "BBB")
        self.assertRaises(TypeError, auto.check_pattern_alphabet, "AC", 2134)
        self.assertRaises(TypeError, auto.check_pattern_alphabet, 1234, "ACA")