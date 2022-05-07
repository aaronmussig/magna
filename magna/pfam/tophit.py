from magna.hmmer.tophit import TopHitFile


class TopHitPfamFile(TopHitFile):
    """The top hit file given the Pfam output."""

    def __init__(self, path: str):
        super().__init__(path)

    def from_pfam_output(self, path: str):
        """Creates a TopHit file from the PFAM output"""
        with open(path, 'r') as f:
            for line in f:
                if line[0] == '#' or not line.strip():
                    continue
                line_split = line.split()
                gene_id = line_split[0]
                hmm_id = line_split[5]
                evalue = float(line_split[12])
                bitscore = float(line_split[11])
                self.add_hit(gene_id, hmm_id, evalue, bitscore)
