import numpy as np
import pandas as pd


def read_pfam(path: str) -> pd.DataFrame:
    """Read the PFAM file.

    Args:
        path: The path to the PFAM file.
    """
    dtype = {
        'seq_id': object,
        'aln_start': np.uintc,
        'aln_end': np.uintc,
        'env_start': np.uintc,
        'env_end': np.uintc,
        'hmm_acc': object,
        'hmm_name': object,
        'type': object,
        'hmm_start': np.uintc,
        'hmm_end': np.uintc,
        'hmm_length': np.float64,
        'bit_score': np.float64,
        'e_value': np.float64,
        'significance': np.float64,
        'clan': object
    }
    lines = list()
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            lines.append(line.split())
    return pd.DataFrame(lines, columns=dtype)


def read_pfam_tophit(path: str) -> pd.DataFrame:
    """Read the PFAM tophit file.

    Args:
        path: The path to the PFAM tophit file.
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
