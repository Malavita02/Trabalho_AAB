from unittest import TestCase
from Trie import Trie

class TestTrie(TestCase):
    def test_insert(self):
        t = Trie("AAA AAG ACTT")
        self.assertRaises(TypeError, t.check_seqs, ["phge"])
        self.assertRaises(TypeError, t.check_seqs, True)
        self.assertRaises(TypeError, t.check_seqs, 1654)

    def test_matches(self):
        t = Trie("AAA AAG ACTT")
        self.assertEqual(t.matches("AAA"), True)
        self.assertEqual(t.matches("TTT"), False)
