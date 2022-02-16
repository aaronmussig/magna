import os
from typing import Dict, Tuple

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from magna.gtdb.enums import GtdbRelease
from magna.io import cache_file


class Genome:

    def __init__(self, accession: str, root: str):
        self.accession: str = accession
        self.root: str = root

        # Generate paths
        base = os.path.basename(self.root)
        self.cds_path = os.path.join(self.root, f'{base}_cds_from_genomic.fna')
        self.fna_path = os.path.join(self.root, f'{base}_genomic.fna')

    def __repr__(self):
        return str(self.accession)

    def cds_seqio(self) -> Tuple[SeqRecord, ...]:
        # Returns the CDS generated from the FNA
        with open(self.cds_path, 'r') as f:
            out = tuple(SeqIO.parse(f, 'fasta'))
        return out

    def fna_seqio(self) -> Tuple[SeqRecord, ...]:
        # Returns the FNA
        with open(self.fna_path, 'r') as f:
            out = tuple(SeqIO.parse(f, 'fasta'))
        return out


class GenomeDirs:

    def __init__(self, release: GtdbRelease):
        self.release = release

        # Create the paths
        srv_path = f'/srv/db/gtdb/genomes/ncbi/release{release.value}/genome_dirs.tsv'
        cache_path = cache_file(srv_path, f'genome_dirs_{self.release.value}.tsv')

        # Read the data
        self._data = self.read(cache_path)

    @staticmethod
    def read(path: str) -> Dict[str, str]:
        out = dict()
        with open(path, 'r') as f:
            for line in f:
                short, root, canonical = line.strip().split('\t')
                out[short] = root
        return out

    def get(self, accession: str) -> Genome:
        return Genome(accession=accession, root=self._data[accession])
