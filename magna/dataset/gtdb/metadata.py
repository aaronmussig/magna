import os
import tempfile

import pandas as pd

from magna.config import MAGNA_DIR
from magna.io import download_file, md5sum, untar


class _GtdbMetadataR95:

    def __init__(self, source: str, path: str, md5: str):
        self.source = source
        self.path = path
        self.md5 = md5
        if not os.path.isfile(self.path):
            self._download()
        self.df = self._read()

    def _read(self):
        df = pd.read_feather(self.path)
        df.set_index('accession')
        return df

    @staticmethod
    def _read_tsv(path):
        return pd.read_csv(path, sep='\t', index_col=False, low_memory=False)

    def _download(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Download
            tmp_path_gz = os.path.join(tmpdir, 'metadata.tar.gz')
            download_file(self.source, tmp_path_gz)

            # Extract and validate
            untar(tmp_path_gz, tmpdir)
            tmp_path = os.path.join(tmpdir, os.path.basename(self.path).replace('.feather', '.tsv'))
            if md5sum(tmp_path) != self.md5:
                raise ValueError('MD5 checksum mismatch')

            df = self._read_tsv(tmp_path)
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            df.to_feather(path=self.path, compression='lz4')


class GtdbMetadataR95Arc(_GtdbMetadataR95):
    source = 'https://data.gtdb.ecogenomic.org/releases/release95/95.0/ar122_metadata_r95.tar.gz'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'ar122_metadata_r95.feather')
    md5 = '110ad5daa2dbed2ee904b10c295da5dc'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR95Bac(_GtdbMetadataR95):
    source = 'https://data.ace.uq.edu.au/public/gtdb/data/releases/release95/95.0/bac120_metadata_r95.tar.gz'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'bac120_metadata_r95.feather')
    md5 = '223ada02ffca4d1a2dda6edb9a164dcd'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR95:

    def __init__(self):
        self.df = pd.concat([GtdbMetadataR95Arc().df, GtdbMetadataR95Bac().df])
