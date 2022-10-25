from typing import Tuple, Optional, Iterator


class Hit(object):
    """More significant hits have a higher bit-score and lower e-value.

    Running sorted() on a list of Hit objects will yield a list in order of
    least significant to most significant hits.
    """

    def __eq__(self, other) -> bool:
        """Returns True if self is equal to other."""

    def __lt__(self, other) -> bool:
        """Is self less significant than other?"""

    @property
    def gene_id(self) -> str:
        """Return the gene id"""

    @property
    def hmm_id(self) -> str:
        """Return the HMM id"""

    @property
    def e_val(self) -> float:
        """e val"""

    @property
    def bit_score(self) -> float:
        """bit score"""

    def hmm_str(self) -> str:
        """Report the e-value and bit-score for the hmm."""


class TopHitFile:
    """Stores information about the top marker hits for Pfam/TIGRFAM markers."""

    def __init__(self, path: str):
        """Setup the path to the file and initialise storage dictionary."""

    def add_hit(self, gene_id: str, hmm_id: str, e_val: float, bit_score: float):
        """Store the most significant HMM hit for each gene."""

    def contains_gene_id(self, gene_id: str) -> bool:
        """Returns True if the gene_id is found in the top hit file."""

    def contains_gene_hmm(self, gene_id: str, hmm_id: str) -> bool:
        """Returns True if there is a hmm hit for the gene_id."""

    def get_top_hit(self, gene_id: str) -> Optional[Hit]:
        """Returns the most significant hit for a given gene id or None."""

    def get_hmm_hit(self, gene_id: str, hmm_id: str) -> Hit:
        """Returns the hit indexed by the gene and hmm id."""

    def write(self):
        """Writes the file to disk and creates a checksum."""

    def read(self):
        """Read the contents of an existing tophit file."""

    def iter_hits(self) -> Iterator[Tuple[str, Hit]]:
        """Iterate over all genes and their respective hits."""
