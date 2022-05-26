from unittest import TestCase
import EvolAlgorithm as EA

class TestEvolAlgorithm(TestCase):
    def test_run(self):
        ea = EA.EvolAlgorithm(popsize=1000, numits=1000, noffspring=800, indsize=50)
        self.assertEqual(ea.get_best_fit(), 49.0)
