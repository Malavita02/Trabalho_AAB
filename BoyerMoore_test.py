import unittest
from BoyerMoore import BoyerMoore

class TestBoyerMoore(unittest.TestCase):
    def test_search_pattern(self):
        bm = BoyerMoore("ACCA", "ACTG")
        self.assertEqual(bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"), [5, 13, 23, 37])
        bm = BoyerMoore("AGACG", "ACTG")
        self.assertEqual(bm.search_pattern("ATAGACGGTATTTGTCCATACAAAGGTAGACGTTATGGAACCTGTC"), [2, 27])

    def test_types(self):
        bm = BoyerMoore("AGACG", "ACTG")
        self.assertRaises(TypeError, bm, "phge")


