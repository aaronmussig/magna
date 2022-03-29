import numpy as np
import pandas as pd

DIAMOND_DTYPE = {
    'query': object,
    'reference': object,
    'identity': np.float64,
    'length': np.uintc,
    'mismatches': np.uintc,
    'gap_openings': np.uintc,
    'query_start': np.uintc,
    'query_end': np.uintc,
    'target_start': np.uintc,
    'target_end': np.uintc,
    'e_value': np.float64,
    'bit_score': np.float64,
}


def read_diamond_output(path: str) -> pd.DataFrame:
    """Return a pandas DataFrame from a DIAMOND output file.

    Columns:
        * ``query`` - the accession of the sequence that was searched against the database, as specified in the input FASTA file after the > character until the first blank.
        * ``reference`` - the accession of the target database sequence that the query was aligned against
        * ``identity`` - the percentage of identical amino acid residues that were aligned against each other in the local alignment
        * ``length`` - the total length of the local alignment, which including matching and mismatching positions of query and subject, as well as gap positions in the query and subject.
        * ``mismatches`` - the number of non-identical amino acid residues aligned against each other.
        * ``gap_openings`` - the number of gap openings.
        * ``query_start`` - the starting coordinate of the local alignment in the query (1-based).
        * ``query_end`` - the ending coordinate of the local alignment in the query (1-based).
        * ``target_start`` - the starting coordinate of the local alignment in the subject (1-based).
        * ``target_end`` - the ending coordinate of the local alignment in the subject (1-based).
        * ``e_value`` - the expected value of the hit quantifies the number of alignments of similar or better quality that you expect to find searching this query against a database of random sequences the same size as the actual target database. This number is most useful for measuring the significance of a hit. By default, DIAMOND will report all alignments with e-value < 0.001, meaning that a hit of this quality will be found by chance on average once per 1,000 queries.
        * ``bit_score`` - the bit score is a scoring matrix independent measure of the (local) similarity of the two aligned sequences, with higher numbers meaning more similar. It is always >= 0 for local Smith Waterman alignments.

    Args:
        path: The path to the DIAMOND output file.
    """
    return pd.read_csv(path, sep='\t', header=None, names=DIAMOND_DTYPE.keys(),
                       dtype=DIAMOND_DTYPE)
