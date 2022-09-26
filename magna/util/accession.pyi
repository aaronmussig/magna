def canonical_gid(gid: str) -> str:
    """Get canonical form of NCBI genome accession.

    Args:
        gid: The NCBI genome accession.

    Example:
        >>> canonical_gid('GCF_005435135.1_ASM543513v1_genomic')
        'G005435135'
    """
