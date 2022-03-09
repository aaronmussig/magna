import os

import pandas as pd

from magna.config import MAGNA_DIR


def gunc_max_css_scores_gtdb_r95() -> pd.DataFrame:
    path = os.path.join(MAGNA_DIR, 'dataset', 'gunc', 'GUNC.gtdb_95.maxCSS_level.feather')
    if not os.path.isfile(path):
        raise IOError(f'{path} does not exist.')
    return pd.read_feather(path)


def gunc_contig_assignment_gtdb_r95() -> pd.DataFrame:
    path = os.path.join(MAGNA_DIR, 'dataset', 'gunc', 'GUNC.gtdb_95.contig_assignments.feather')
    if not os.path.isfile(path):
        raise IOError(f'{path} does not exist.')
    return pd.read_feather(path)


def gunc_all_levels_gtdb_r95() -> pd.DataFrame:
    path = os.path.join(MAGNA_DIR, 'dataset', 'gunc', 'gtdb_95.all_levels.tsv')
    if not os.path.isfile(path):
        raise IOError(f'{path} does not exist.')
    return pd.read_feather(path)
