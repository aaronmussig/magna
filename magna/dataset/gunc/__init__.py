import os
import shutil
import tempfile

import numpy as np
import pandas as pd

from magna.config import MAGNA_DIR
from magna.io import download_file


class GuncAllScores:
    source = 'https://swifter.embl.de/~fullam/gunc/paper_supplementary_files/All_Datasets.GUNC.scores.all_levels.specI2species.tsv'
    path = os.path.join(MAGNA_DIR, 'dataset', 'gunc', 'All_Datasets.GUNC.scores.all_levels.specI2species.tsv')
    md5 = 'a54e3719221a42a5f96b267412827d27'

    def __init__(self):
        if not os.path.isfile(self.path):
            self._download()
        self.df = self._read()

    def _read(self):
        dtype = {
            'n_genes_called': np.uintc,
            'n_genes_mapped': np.uintc,
            'n_contigs': np.uintc,
            'proportion_genes_retained_in_major_clades': np.float16,
            'genes_retained_index': np.float16,
            'clade_separation_score': np.float16,
            'contamination_portion': np.float16,
            'n_effective_surplus_clades': np.float16,
            'mean_hit_identity': np.float16,
            'reference_representation_score': np.float16,
        }
        converters = {'pass.GUNC': lambda x: x == 'True'}
        print(f'Note: Line 1,934,122 is skipped as GMGC.SAMEA2623756.bin.19 (GMGC unfiltered) is NaN.')
        df = pd.read_csv(self.path, sep='\t', index_col=False, dtype=dtype,
                         converters=converters, skiprows=[1934122])
        return df

    def _download(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Download the file
            tmp_path = os.path.join(tmpdir, 'download.tsv')
            download_file(self.source, tmp_path, self.md5)

            # Move the file
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            shutil.move(tmp_path, self.path)
