import os
import tempfile

import numpy as np
import pandas as pd

from magna.config import MAGNA_DIR
from magna.util.io import download_file


def read_contig_assignments_tsv(path: str) -> pd.DataFrame:
    """Read from the GUNC contig_assignments output file.

    Args:
        path: The path to the DIAMOND output file.
    """
    dtype = {
        'contig': object,
        'tax_level': object,
        'assignment': object,
        'count_of_genes_assigned': np.uintc
    }
    return pd.read_csv(path, sep='\t', dtype=dtype)


def gunc_max_css_scores_gtdb_r95() -> pd.DataFrame:
    """Return the max clade separation score (CSS) for the R95 GTDB."""
    path = os.path.join(MAGNA_DIR, 'gunc', 'gtdb_95.maxcss_level.feather')
    if not os.path.isfile(path):
        raise IOError(f'{path} does not exist.')
    return pd.read_feather(path)


def gunc_contig_assignment_gtdb_r95() -> pd.DataFrame:
    """Return the contig assignment for the R95 GTDB."""
    path = os.path.join(MAGNA_DIR, 'gunc', 'gtdb_95.contig_assignments.feather')
    if not os.path.isfile(path):
        raise IOError(f'{path} does not exist.')
    return pd.read_feather(path)


def gunc_all_levels_gtdb_r95() -> pd.DataFrame:
    """Return GUNC output at all levels for the R95 GTDB."""
    path = os.path.join(MAGNA_DIR, 'gunc', 'gtdb_95.all_levels.feather')
    if not os.path.isfile(path):
        raise IOError(f'{path} does not exist.')
    return pd.read_feather(path)


class GuncMaxCssScores:
    """Return the max clade separation score (CSS) for the R95 GTDB (progenes db)."""

    source = 'https://swifter.embl.de/~fullam/gunc/paper_supplementary_files/All_Datasets.GUNC.scores.maxCSS_level.tsv'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gunc', 'All_Datasets.GUNC.scores.maxCSS_level.feather')
    md5 = 'dd91aa177b9112c361b9503e132f1c06'

    def __init__(self):
        if not os.path.isfile(self.path):
            self._download()
        #: The dataframe.
        self.df: pd.DataFrame = self._read()

    def _read(self):
        print('Note: Only the RefSeq and GenBank results are used.')
        return pd.read_feather(self.path)

    @staticmethod
    def _read_tsv(path):
        dtype = {
            'genome': np.object,
            'n_genes_called': np.uintc,
            'n_genes_mapped': np.uintc,
            'n_contigs': np.uintc,
            'taxonomic_level': np.object,
            'proportion_genes_retained_in_major_clades': np.float16,
            'genes_retained_index': np.float16,
            'clade_separation_score': np.float16,
            'contamination_portion': np.float16,
            'n_effective_surplus_clades': np.float16,
            'mean_hit_identity': np.float16,
            'reference_representation_score': np.float16,
            'pass.GUNC': np.object,
            'study': np.object,
            'CheckM_completeness': np.object,
            'CheckM_contamination': np.object,
        }
        rows = list()
        allowed_studies = frozenset({'GenBank', 'RefSeq'})
        with open(path, 'r') as f:
            header = {k: i for i, k in enumerate(
                f.readline().strip().split('\t'))}
            study_idx = header['study']
            for line in f.readlines():
                cols = line.strip().split('\t')
                if cols[study_idx] in allowed_studies:
                    rows.append(cols)
        return pd.DataFrame(rows, columns=dtype)

    def _download(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Download the file
            tmp_path = os.path.join(tmpdir, 'download.tsv')
            download_file(self.source, tmp_path, self.md5)

            df = self._read_tsv(tmp_path)
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            df.to_feather(path=self.path, compression='lz4')


class GuncAllScores:
    """Return GUNC output at all levels for the R95 GTDB (progenes db)."""

    source = 'https://swifter.embl.de/~fullam/gunc/paper_supplementary_files/All_Datasets.GUNC.scores.all_levels.specI2species.tsv'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gunc', 'All_Datasets.GUNC.scores.all_levels.specI2species.feather')
    md5 = 'a54e3719221a42a5f96b267412827d27'

    def __init__(self):
        if not os.path.isfile(self.path):
            self._download()
        #: The dataframe.
        self.df: pd.DataFrame = self._read()

    def _read(self):
        print('Note: Only the RefSeq and GenBank results are used.')
        return pd.read_feather(self.path)

    @staticmethod
    def _read_tsv(path):
        dtype = {
            'genome': np.object,
            'n_genes_called': np.uintc,
            'n_genes_mapped': np.uintc,
            'n_contigs': np.uintc,
            'taxonomic_level': np.object,
            'proportion_genes_retained_in_major_clades': np.float16,
            'genes_retained_index': np.float16,
            'clade_separation_score': np.float16,
            'contamination_portion': np.float16,
            'n_effective_surplus_clades': np.float16,
            'mean_hit_identity': np.float16,
            'reference_representation_score': np.float16,
            'pass.GUNC': np.object,
            'study': np.object,
        }
        rows = list()
        allowed_studies = frozenset({'GenBank', 'RefSeq'})
        with open(path, 'r') as f:
            header = {k: i for i, k in enumerate(
                f.readline().strip().split('\t'))}
            study_idx = header['study']
            for line in f.readlines():
                cols = line.strip().split('\t')
                if cols[study_idx] in allowed_studies:
                    rows.append(cols)
        return pd.DataFrame(rows, columns=dtype)

    def _download(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Download the file
            tmp_path = os.path.join(tmpdir, 'download.tsv')
            download_file(self.source, tmp_path, self.md5)

            df = self._read_tsv(tmp_path)
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            df.to_feather(path=self.path, compression='lz4')
