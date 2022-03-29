import numpy as np
import pandas as pd


def read_tigrfam(path: str) -> pd.DataFrame:
    """Read the TIGRFAM file.

    Args:
        path: The path to the TIGRFAM file.
    """
    dtype = {
        'seq_id': object,
        'hmm_acc': object,
        'full_seq_e_value': np.float64,
        'full_seq_score': np.float64,
        'full_seq_bias': np.float64,
        'best_domain_e_value': np.float64,
        'best_domain_score': np.float64,
        'best_domain_bias': np.float64,
        'exp': np.float64,
        'reg': np.float64,
        'clu': np.float64,
        'ov': np.float64,
        'env': np.float64,
        'dom': np.float64,
        'rep': np.float64,
        'inc': np.float64,
        'description': object,
    }
    lines = list()
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            cols = line.split()
            cur_line = [cols[0], cols[3]]
            cur_line.extend(cols[4:18])
            cur_line.append(' '.join(cols[18:]))
            lines.append(cur_line)
    return pd.DataFrame(lines, columns=dtype)


def read_tigrfam_tophit(path: str) -> pd.DataFrame:
    """Read the TIGRFAM tophit file.

    Args:
        path: The path to the TIGRFAM tophit file.
    """
    dtype = {
        'seq_id': object,
        'pfam_acc': object,
        'e_value': np.float64,
        'bit_score': np.uintc,
    }
    lines = list()
    with open(path, 'r') as f:
        f.readline()
        for line in f.readlines():
            line = line.strip()
            gene_id, hits = line.split('\t')
            for hit in hits.split(';'):
                pfam_acc, e_val, bit_score = hit.split(',')
                lines.append([gene_id, pfam_acc, e_val, bit_score])
    return pd.DataFrame(lines, columns=dtype)
