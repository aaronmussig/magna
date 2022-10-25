import time
import unittest

from magna.hmmer.tophit import TopHitFile


class TestBindings(unittest.TestCase):

    def test_add_node(self):
        n = 1

        c = time.time()
        th = TopHitFile('/tmp/bar.txt')
        for _ in range(n):
            th.add_hit("a", "b", 1.23, 3.45)
            th.add_hit("a", "c", 1.24, 44)
            th.add_hit("a", "d", 1.24, 3.42)
            th.add_hit("a", "d", 1.24, 3.41)
            x = th.get_top_hit("a")
            th.write()

            th2 = TopHitFile('/tmp/bar.txt')
            th2.read()

        d = time.time()
        print(d - c)

        return
