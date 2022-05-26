from unittest import TestCase
from MotifFinding import MotifFinding
from MySeq import MySeq

class TestMotifFinding(TestCase):

    def test_score(self):
        mf = MotifFinding()
        mf.readFile("exemploMotifs.txt", "dna")
        self.assertEqual(mf.score([25, 20, 2, 55, 59]), 30)
        self.assertEqual(mf.score([1, 4, 45, 5, 0]), 34)
        self.assertEqual(mf.score([0, 38, 14, 33, 1]), 30)
        self.assertEqual(mf.score([22, 33, 23, 32, 15]), 26)
        self.assertEqual(mf.score([52, 21, 60, 54, 50]), 20)

    def test_score_mult(self):
        mf = MotifFinding()
        mf.readFile("exemploMotifs.txt", "dna")
        self.assertEqual(mf.scoreMult([25, 20, 2, 55, 59]), 0.08847360000000001)
        self.assertEqual(mf.scoreMult([16, 13, 43, 27, 0]), 0.0221184)
        self.assertEqual(mf.scoreMult([44, 11, 27, 30, 6]), 0.0026214400000000014)

    def test_exhaustive_search(self):
        mf = MotifFinding(3, [MySeq("ATAGAGCTGA", "dna"), MySeq("ACGTAGATGA", "dna"), MySeq("AAGATAGGGG", "dna")])
        self.assertEqual(mf.exhaustiveSearch(), [1, 3, 4])

    def test_branch_and_bound(self):
        mf = MotifFinding(3, [MySeq("ATAGAGCTGA", "dna"), MySeq("ACGTAGATGA", "dna"), MySeq("AAGATAGGGG", "dna")])
        self.assertEqual(mf.branchAndBound(), [1, 3, 4])
        mf = MotifFinding()
        mf.readFile("exemploMotifs.txt", "dna")
        self.assertEqual(mf.branchAndBound(), [1, 4, 45, 5, 0])

    def test_heuristic_consensus(self):
        mf = MotifFinding()
        mf.readFile("exemploMotifs.txt", "dna")
        self.assertEqual(mf.heuristicConsensus(), [0, 38, 14, 33, 1])
        mf = MotifFinding()
        mf.readFile("exemploMotifs2.txt", "dna")
        self.assertEqual(mf.heuristicConsensus(), [25, 20, 2, 55, 59])

    def test_heuristic_stochastic(self):
        mf = MotifFinding()
        mf.readFile("exemploMotifs.txt", "dna")
        self.assertEqual(type(mf.heuristicStochastic()), list)

    def test_gibbs(self):
        mf = MotifFinding()
        mf.readFile("exemploMotifs.txt", "dna")
        self.assertEqual(type(mf.gibbs()), list)


