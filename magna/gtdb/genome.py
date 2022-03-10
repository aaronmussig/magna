import os
from typing import Dict, Tuple

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from magna.gtdb.enums import GtdbRelease
from magna.util.io import cache_file


class Genome:
    """A wrapper to a GTDB genome."""

    def __init__(self, accession: str, root: str):
        #: The short accession of the genome.
        self.accession: str = accession
        #: The root directory where this genome is stored.
        self.root: str = root

        # Generate paths
        base = os.path.basename(self.root)
        #: The path to the CDS file.
        self.cds_path: str = os.path.join(self.root, f'{base}_cds_from_genomic.fna')
        #: The path to the FNA file.
        self.fna_path: str = os.path.join(self.root, f'{base}_genomic.fna')

    def __repr__(self):
        return str(self.accession)

    def cds_seqio(self) -> Tuple[SeqRecord, ...]:
        """Read and return the CDS file as a SeqIO object."""
        with open(self.cds_path, 'r') as f:
            out = tuple(SeqIO.parse(f, 'fasta'))
        return out

    def fna_seqio(self) -> Tuple[SeqRecord, ...]:
        """Read and return the FNA file as a SeqIO object."""
        with open(self.fna_path, 'r') as f:
            out = tuple(SeqIO.parse(f, 'fasta'))
        return out


class GenomeDirs:
    """An interface to the :obj:`GtdbRelease` accession to :obj:`Genome` mapping."""

    def __init__(self, release: GtdbRelease):
        """Initialise the GenomeDirs class for a given release.

        Args:
            release: The release of GTDB to use.
        """
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
        """Return the :obj:`Genome` for the given accession.

        Args:
            accession: The short accession of the genome (e.g. ``GCA_123456789.1``).
        """
        return Genome(accession=accession, root=self._data[accession])
