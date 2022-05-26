from unittest import TestCase
from SufixTrie import Sufix_trie

class TestSufix_trie(TestCase):
    def test_insert(self):
        st = Sufix_trie("TACTA")
        self.assertRaises(TypeError, st, ["phge"])
        self.assertRaises(TypeError, st, True)
        self.assertRaises(TypeError, st, 1654)

    def test_matches(self):
        st = Sufix_trie("TACTA")
        self.assertEqual(st.matches("TA"), [0,3])
        self.assertEqual(st.matches("AT"), False)
