import os
import tempfile

from Bio import SeqIO

from magna.config import MAGNA_DIR
from magna.util.disk import md5sum, untar, move_file
from magna.util.web import download_file


class GtdbSsu:
    """The base class that all GTDB SSU objects inherit."""

    __slots__ = ('source', 'path', 'md5', 'fna')

    def __init__(self, source: str, path: str, md5: str):
        #: The source URL.
        self.source: str = source
        #: The path to the downloaded file.
        self.path: str = path
        #: The expected MD5 checksum of the file.
        self.md5: str = md5
        if not os.path.isfile(self.path):
            self._download()
        #: The FNA.
        self.fna = self._read_fasta(self.path)

    @staticmethod
    def _read_fasta(path: str):
        with open(path) as f:
            d_results = SeqIO.to_dict(SeqIO.parse(f, 'fasta'))
            return {k: v for k, v in d_results.items()}

    def _download(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path_gz = os.path.join(tmpdir, 'ssu.tar.gz')
            tmp_path_fna = os.path.join(tmpdir, 'ssu_all_r207.fna')
            download_file(self.source, tmp_path_gz)
            untar(tmp_path_gz, tmpdir)

            if md5sum(tmp_path_fna) != self.md5:
                raise ValueError('MD5 checksum mismatch')

            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            move_file(tmp_path_fna, self.path)


class GtdbBacSsuR207(GtdbSsu):
    """GTDB SSU for representative genomes in R207"""
    source = 'https://data.gtdb.ecogenomic.org/releases/release207/207.0/genomic_files_all/ssu_all_r207.tar.gz'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'ssu', 'bac120_ssu_r207.fna')
    md5 = '95f2cdf1cf8fa76aa32f54ee5f56e251'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)
