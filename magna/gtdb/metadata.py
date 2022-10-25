import os
import tempfile

import pandas as pd

from magna.config import MAGNA_DIR
from magna.util.disk import md5sum, untar
from magna.util.web import download_file


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
            tmp_path_dl = os.path.join(tmpdir, os.path.basename(self.source))
            download_file(self.source, tmp_path_dl)

            # Extract
            if tmp_path_dl.endswith('.gz'):
                untar(tmp_path_dl, tmpdir)
                tmp_path = os.path.join(tmpdir, os.path.basename(self.path).replace('.feather', '.tsv'))
            else:
                tmp_path = tmp_path_dl

            # Validate
            md5 = md5sum(tmp_path)
            if md5 != self.md5:
                raise ValueError(f'MD5 checksum mismatch: {md5} != {self.md5}')

            df = self._read_tsv(tmp_path)
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            df.to_feather(path=self.path, compression='lz4')


# ----------------------------------------------------------------------------------------------------------------------


class GtdbMetadataR80Bac(GtdbMetadata):
    """The bacterial metadata."""

    source = 'https://data.gtdb.ecogenomic.org/releases/release80/80.0/bac_metadata_r80.tsv'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'bac120_metadata_r80.feather')
    md5 = '28bad432335306f32b6872f819a66f0c'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR80:
    """The combined archaeal and bacterial metadata."""

    def __init__(self):
        #: The combined dataframe.
        self.df: pd.DataFrame = GtdbMetadataR80Bac().df


# ----------------------------------------------------------------------------------------------------------------------


class GtdbMetadataR83Bac(GtdbMetadata):
    """The bacterial metadata."""

    source = 'https://data.gtdb.ecogenomic.org/releases/release83/83.0/bac_metadata_r83.tsv'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'bac120_metadata_r83.feather')
    md5 = 'de08ec5515261e8f904bb11d14da7d24'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR83:
    """The combined archaeal and bacterial metadata."""

    def __init__(self):
        #: The combined dataframe.
        self.df: pd.DataFrame = GtdbMetadataR83Bac().df


# ----------------------------------------------------------------------------------------------------------------------

class GtdbMetadataR86Arc(GtdbMetadata):
    """The archaeal metadata."""

    source = 'https://data.gtdb.ecogenomic.org/releases/release86/86.2/ar122_metadata_r86.2.tsv'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'ar122_metadata_r86.2.feather')
    md5 = 'a91fc39cc9c4a73f3110b24462f30245'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR86Bac(GtdbMetadata):
    """The bacterial metadata."""

    source = 'https://data.gtdb.ecogenomic.org/releases/release86/86.2/bac120_metadata_r86.2.tsv'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'bac120_metadata_r86.2.feather')
    md5 = '1448d67748e9308056ca32c59ac17837'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR86:
    """The combined archaeal and bacterial metadata."""

    def __init__(self):
        #: The combined dataframe.
        self.df: pd.DataFrame = pd.concat([GtdbMetadataR86Arc().df, GtdbMetadataR86Bac().df])


# ----------------------------------------------------------------------------------------------------------------------

class GtdbMetadataR89Arc(GtdbMetadata):
    """The archaeal metadata."""

    source = 'https://data.gtdb.ecogenomic.org/releases/release89/89.0/ar122_metadata_r89.tsv'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'ar122_metadata_r89.feather')
    md5 = '7f10b53490c3c764fb75b72d1445e93e'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR89Bac(GtdbMetadata):
    """The bacterial metadata."""

    source = 'https://data.gtdb.ecogenomic.org/releases/release89/89.0/bac120_metadata_r89.tsv'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'bac120_metadata_r89.feather')
    md5 = 'ff55a34f988469ceb71536af996d5739'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR89:
    """The combined archaeal and bacterial metadata."""

    def __init__(self):
        #: The combined dataframe.
        self.df: pd.DataFrame = pd.concat([GtdbMetadataR89Arc().df, GtdbMetadataR89Bac().df])


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


class GtdbMetadataR207Arc(GtdbMetadata):
    """The archaeal metadata (release 207)."""

    source = 'https://data.gtdb.ecogenomic.org/releases/release207/207.0/ar53_metadata_r207.tar.gz'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'ar53_metadata_r207.feather')
    md5 = 'cd99ab8c55fffac51ab05c9510b07f67'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR207Bac(GtdbMetadata):
    """The bacterial metadata (release 207)."""
    source = 'https://data.gtdb.ecogenomic.org/releases/release207/207.0/bac120_metadata_r207.tar.gz'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gtdb', 'metadata', 'bac120_metadata_r207.feather')
    md5 = 'f46495420129e04010288321110b15eb'

    def __init__(self):
        super().__init__(self.source, self.path, self.md5)


class GtdbMetadataR207:
    """The combined archaeal and bacterial metadata (release 207)."""

    def __init__(self):
        #: The combined dataframe.
        self.df: pd.DataFrame = pd.concat([GtdbMetadataR207Arc().df, GtdbMetadataR207Bac().df])
