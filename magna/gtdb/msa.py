import os
import tempfile

from Bio import SeqIO

from magna.config import MAGNA_DIR
from magna.util.disk import md5sum, untar, move_file
from magna.util.web import download_file


class GtdbMsa:
    """The base class that all GTDB MSA objects inherit."""

    __slots__ = ('source', 'path', 'md5', 'faa')

    def __init__(self, source: str, path: str, md5: str):
        #: The source URL.
        self.source: str = source
        #: The path to the downloaded file.
        self.path: str = path
        #: The expected MD5 checksum of the file.
        self.md5: str = md5
        if not os.path.isfile(self.path):
            self._download()
        #: The FAA.
        self.faa = self._read_fasta(self.path)

    @staticmethod
    def _read_fasta(path: str):
        with open(path) as f:
            d_results = SeqIO.to_dict(SeqIO.parse(f, 'fasta'))
            return {k: v for k, v in d_results.items()}

    def _download(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path_gz = os.path.join(tmpdir, 'bac120_msa_reps_r207.tar.gz')
            tmp_path_fna = os.path.join(tmpdir, 'bac120_msa_reps_r207.faa')
            download_file(self.source, tmp_path_gz)
            untar(tmp_path_gz, tmpdir)

            if md5sum(tmp_path_fna) != self.md5:
                raise ValueError(f'MD5 checksum mismatch: {tmp_path_fna}')

            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            move_file(tmp_path_fna, self.path)


class GtdbBacMsaR207(GtdbMsa):
    """GTDB MSA for representative genomes in R207"""
    source = 'https://data.gtdb.ecogenomic.org/releases/release207/207.0/genomic_files_reps/bac120_msa_reps_r207.tar.gz'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'msa', 'bac120_msa_reps_r207.faa')
    md5 = '40bf3b10526bac42024b99c669306738'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)
