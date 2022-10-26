import unittest

from magna.kmer import get_kmer_count_seq


class TestBindings(unittest.TestCase):

    def test_kmer_count_seq(self):
        seq = 'ATCGATAGATTAAA'
        x = get_kmer_count_seq(seq, 2, True)
