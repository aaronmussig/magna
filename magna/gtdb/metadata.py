import os
import tempfile

import pandas as pd

from magna.config import MAGNA_DIR
from magna.util.io import download_file, md5sum, untar


class GtdbMetadata:

    def __init__(self, source: str, path: str, md5: str):
        #: The source URL
        self.source: str = source
        #: The path to the metadata file.
        self.path: str = path
        #: The MD5 checksum of the downloaded file.
        self.md5: str = md5
        if not os.path.isfile(self.path):
            self._download()
        #: The metadata as a pandas DataFrame.
        self.df: pd.DataFrame = self._read()

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


# ----------------------------------------------------------------------------------------------------------------------

class GtdbMetadataR95Arc(GtdbMetadata):
    """The archaeal metadata (release 95)."""

    source = 'https://data.gtdb.ecogenomic.org/releases/release95/95.0/ar122_metadata_r95.tar.gz'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'ar122_metadata_r95.feather')
    md5 = '110ad5daa2dbed2ee904b10c295da5dc'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR95Bac(GtdbMetadata):
    """The bacterial metadata (release 95)."""

    source = 'https://data.gtdb.ecogenomic.org/releases/release95/95.0/bac120_metadata_r95.tar.gz'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'bac120_metadata_r95.feather')
    md5 = '223ada02ffca4d1a2dda6edb9a164dcd'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR95:
    """The combined archaeal and bacterial metadata (release 95)."""

    def __init__(self):
        #: The combined dataframe.
        self.df: pd.DataFrame = pd.concat([GtdbMetadataR95Arc().df, GtdbMetadataR95Bac().df])


# ----------------------------------------------------------------------------------------------------------------------

class GtdbMetadataR202Arc(GtdbMetadata):
    """The archaeal metadata (release 202)."""

    source = 'https://data.gtdb.ecogenomic.org/releases/release202/202.0/ar122_metadata_r202.tar.gz'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'ar122_metadata_r202.feather')
    md5 = '0607728ae1f56bdb1a7cc24d238185c3'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR202Bac(GtdbMetadata):
    """The bacterial metadata (release 202)."""
    source = 'https://data.gtdb.ecogenomic.org/releases/release202/202.0/bac120_metadata_r202.tar.gz'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'bac120_metadata_r202.feather')
    md5 = '68fed11eb688982edb6f4669476c2a10'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR202:
    """The combined archaeal and bacterial metadata (release 202)."""

    def __init__(self):
        #: The combined dataframe.
        self.df: pd.DataFrame = pd.concat([GtdbMetadataR202Arc().df, GtdbMetadataR202Bac().df])

# ----------------------------------------------------------------------------------------------------------------------
