from unittest import TestCase
from Bwt import Bwt


class TestBwt(TestCase):

    def test_get_bwt(self):
        bwt = Bwt("TAGACAGAGA$")
        self.assertEqual(bwt.get_bwt(), "AGGGTCAAAA$")
        bwt = Bwt("ACTAGAGACA$")
        self.assertEqual(bwt.get_bwt(), "ACG$GTAAAAC")

    def test_reverse_bwt(self):
        bwt = Bwt("TAGACAGAGA$")
        self.assertEqual(bwt.reverse_bwt("AGGGTCAAAA$"), "TAGACAGAGA")
        bwt = Bwt("ACTAGAGACA$")
        self.assertEqual(bwt.reverse_bwt("ACG$GTAAAAC"), "ACTAGAGACA")

    def test_find_pattern(self):
        bwt = Bwt("TAGACAGAGA$")
        bwt.reverse_bwt("AGGGTCAAAA$")
        self.assertEqual(bwt.find_pattern("AGA"), [3, 4, 5])

    def test_types(self):
        bwt = Bwt("TAGACAGAGA$")
        self.assertRaises(TypeError, bwt, ["phge"])
        self.assertRaises(TypeError, bwt, True)
        self.assertRaises(TypeError, bwt, 1654)

