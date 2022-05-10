import urllib
import urllib.request
from typing import Optional

from magna.util.disk import TqdmUpTo, md5sum


def download_file(url: str, path: str, md5: Optional[str] = None, silent: bool = False):
    """Downloads a file to disk, optionally validating the md5 hash.

    Args:
        url: The url to download from.
        path: The path to save the file to.
        md5: The expected md5 hash of the file.
        silent: True if the progress should be supressed.

    Raises:
        IOError: If the md5 hash doesn't match.

    Examples:
        Download the file at ``https://www.example.com/data.csv`` to ``/tmp/data.csv``.

        >>> download_file('https://www.example.com/data.csv', '/tmp/data.csv')
    """
    if not silent:
        with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=url.split('/')[-1]) as t:
            urllib.request.urlretrieve(url, filename=path, reporthook=t.update_to, data=None)
            t.total = t.n
    else:
        urllib.request.urlretrieve(url, filename=path)

    if md5 and md5 != md5sum(path):
        raise IOError('Hash mismatch')
