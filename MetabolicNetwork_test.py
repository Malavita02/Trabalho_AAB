from unittest import TestCase
from MetabolicNetwork import MetabolicNetwork

class TestMetabolicNetwork(TestCase):
    def test_type(self):
        m = MetabolicNetwork("metabolite-reaction")
        m.add_vertex_type("R1", "reaction")
        m.add_edge("M1", "R1")
        self.assertRaises(TypeError, m.check_type_error_vertex, 123, "reacao")
        self.assertRaises(TypeError, m.check_type_error_network_type, "reacao__reacao")
        self.assertRaises(TypeError, m.check_TypeError_node, ["fasf"])

