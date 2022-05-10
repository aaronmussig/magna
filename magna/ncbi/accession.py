import re

RE_NCBI_ACCESSION = re.compile(r'(GC[AF]_\d{9}\.\d)')


def is_valid_ncbi_gid(gid: str) -> bool:
    """Check if the NCBI accession matches the expected format.

    Args:
        gid: The NCBI accession to check.

    Returns:
        True if the accession is valid, False otherwise.

    Examples:
        >>> is_valid_ncbi_gid('GC_000001.1')
        False

        >>> is_valid_ncbi_gid('GCA_123456789.1')
        True
    """
    return RE_NCBI_ACCESSION.match(gid) is not None
