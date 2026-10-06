"""Indexed native grants retain exact single-range containment."""
import random
import unittest

from tools import native_oracle as oracle


class NativeRangeIndexTests(unittest.TestCase):
    def test_adjacent_grants_do_not_authorize_a_straddling_access(self):
        index=oracle._RangeIndex.build(((100,4),(104,4)))
        self.assertTrue(index.within(100,4))
        self.assertTrue(index.within(104,4))
        self.assertFalse(index.within(102,4))

    def test_overlapping_child_cannot_hide_a_larger_parent_grant(self):
        index=oracle._RangeIndex.build(((100,100),(120,4),(120,2),(160,1)))
        self.assertTrue(index.within(130,70))
        self.assertFalse(index.within(130,71))
        self.assertFalse(index.within(100,0))
        self.assertFalse(index.within(100,-1))

    def test_unsorted_sparse_and_empty_grants_match_original_exhaustively(self):
        rng=random.Random(6210)
        for ranges in((),((50,0),),tuple((rng.randrange(0,80),rng.randrange(0,24))for _ in range(65))):
            index=oracle._RangeIndex.build(ranges)
            for address in range(-1,110):
                for size in range(-1,30):
                    self.assertEqual(index.within(address,size),oracle._within(address,size,ranges),(ranges,address,size))


if __name__=='__main__':unittest.main()
