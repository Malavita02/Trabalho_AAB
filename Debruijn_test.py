from unittest import TestCase
import debruijn as db

class TestDeBruijnGraph(TestCase):

    def test_seq_from_path(self):
        orig_sequence = "ATGCAATGGTCTG"
        frags = db.composition(3, orig_sequence)
        dbgr = db.DeBruijnGraph(frags)
        self.assertIn(frags[0], orig_sequence, "A frag não pertence à sequencia original!")
        p = dbgr.eulerian_path()
        self.assertEqual(dbgr.seq_from_path(p), "ATGCAATGGTCTG")
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC",
                 "TTT"]
        dbgr = db.DeBruijnGraph(frags)
        p = dbgr.eulerian_path()
        self.assertEqual(dbgr.seq_from_path(p), "ACCATTTCATGGCATAA")

    def test_types(self):
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC",
                 "TTT"]
        dbgr = db.DeBruijnGraph(frags)
        self.assertRaises(TypeError, dbgr.check_frags, ["phge"])
        self.assertRaises(TypeError, dbgr.check_frags, True)
        self.assertRaises(TypeError, dbgr.check_frags, 1654)
