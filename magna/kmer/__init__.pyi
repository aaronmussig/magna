from typing import List, Dict

def get_kmer_count_fasta(path: str, k: int, use_rev_complement: bool) -> Dict[str, KmerCountResult]:
    """Return the kmer count for a fasta file."""

def get_kmer_count_seq(seq: str, k: int, use_rev_complement: bool) -> KmerCountResult:
    """Return the k-mer count for a given sequence"""

def get_kmer_to_idx(k: int) -> Dict[str, int]:
    """Return a mapping from each kmer to the index."""

def get_possible_kmers(k: int) -> List[str]:
    """Return all possible kmers for a given value of k."""

class KmerCountResult:
    """A class to store the result of a k-mer count."""

    @property
    def k(self) -> int:
        """Return the value of k."""

    @property
    def total(self) -> int:
        """Return the total number of kmers."""

    @property
    def counts(self) -> List[int]:
        """Return the counts for each kmer."""
