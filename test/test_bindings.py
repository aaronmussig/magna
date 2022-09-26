import unittest

from magna.util.accession import canonical_gid


class TestBindings(unittest.TestCase):

    def test_add_node(self):
        canonical_gid('GBG_CA_005435135.1_ASM543513v1_genomic')
        return
