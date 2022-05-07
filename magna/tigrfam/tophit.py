from magna.hmmer.tophit import TopHitFile, Hit


class TopHitTigrFile(TopHitFile):
    """The top hit file given the Tigrfam output."""

    def __init__(self, path: str):
        super().__init__(path)

    def add_hit(self, gene_id: str, hmm_id: str, e_val: float, bit_score: float):
        """Only store the most significant HMM hit per gene as per GTDBNCBI."""
        if self.contains_gene_id(gene_id):
            # The new hit was more significant, remove any other hits.
            if self.get_top_hit(gene_id) < Hit(gene_id, hmm_id, e_val, bit_score):
                self.hits[gene_id] = dict()
                super().add_hit(gene_id, hmm_id, e_val, bit_score)
        else:
            super().add_hit(gene_id, hmm_id, e_val, bit_score)

    def from_tigrfam_output(self, path: str):
        """Create the top hit file from the Tigrfam output. (i.e. -o)"""
        with open(path, 'r') as f:
            for line in f:
                if line[0] == '#':
                    continue

                line_split = line.split()
                gene_id = line_split[0]
                hmm_id = line_split[3]
                evalue = float(line_split[4])
                bitscore = float(line_split[5])
                self.add_hit(gene_id, hmm_id, evalue, bitscore)
