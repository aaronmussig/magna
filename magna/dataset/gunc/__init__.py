import os
import tempfile
import numpy as np
import pandas as pd

from magna.config import MAGNA_DIR
from magna.io import download_file


class GuncAllScores:
    source = 'https://swifter.embl.de/~fullam/gunc/paper_supplementary_files/All_Datasets.GUNC.scores.all_levels.specI2species.tsv'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gunc', 'All_Datasets.GUNC.scores.all_levels.specI2species.feather')
    md5 = 'a54e3719221a42a5f96b267412827d27'

    def __init__(self):
        if not os.path.isfile(self.path):
            self._download()
        self.df = self._read()

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
