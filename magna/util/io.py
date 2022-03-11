import hashlib
import os
import shutil
import tarfile
import urllib
import urllib.request
from typing import Optional

from tqdm import tqdm

from magna.config import CACHE_DIR


class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        return self.update(b * bsize - self.n)  # also sets self.n = b * bsize


def untar(file_path: str, dir_name: str):
    """Extracts the contents of the tar file into the target directory.

    Args:
        file_path: The path to the tar file.
        dir_name: The directory to extract the tar file into.

    Examples:
        Extract the contents of the tar file at ``/tmp/data.tar.gz`` into the
        directory ``/tmp/data``.

        >>> untar('/tmp/data.tar.gz', '/tmp/data')
    """
    os.makedirs(dir_name, exist_ok=True)
    with tarfile.open(file_path) as tar:
        tar.extractall(dir_name)


def md5sum(path: str) -> str:
    """Returns the md5 hash of a file.

    Args:
        path: The path to the file.
    """
    block_size = 65536
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()


def download_file(url: str, path: str, md5: Optional[str] = None):
    """Downloads a file to disk, optionally validating the md5 hash.

    Args:
        url: The url to download from.
        path: The path to save the file to.
        md5: The expected md5 hash of the file.

    Raises:
        IOError: If the md5 hash doesn't match.

    Examples:
        Download the file at ``https://www.example.com/data.csv`` to ``/tmp/data.csv``.

        >>> download_file('https://www.example.com/data.csv', '/tmp/data.csv')
    """
    with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=path, reporthook=t.update_to, data=None)
        t.total = t.n

    if md5 and md5 != md5sum(path):
        raise IOError('Hash mismatch')


def cache_file(srv_path: str, local_name: str) -> str:
    """Copies a file to the magna cache (doesn't auto-remove).

    Args:
        srv_path: The remote path of the file.
        local_name: The key to cache this file with.

    Returns:
        The path to the cached file.

    Examples:
        Cache the file at ``/srv/data.csv`` as ``data.csv``.

        >>> cache_file('/srv/data.csv', 'data.csv')
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    local_path = os.path.join(CACHE_DIR, local_name)
    if not os.path.isfile(local_path):
        shutil.copyfile(srv_path, local_path)
    return local_path


def copy_file(src: str, dest: str, checksum: Optional[bool] = False):
    """Copies a file from the source path to the destination path.

    Args:
        src: The source path.
        dest: The destination path.
        checksum: Whether to validate the checksum of the file.

    Raises:
        IOError: If the checksum is invalid.
    """
    shutil.copyfile(src, dest)
    if checksum:
        if md5sum(src) != md5sum(dest):
            raise IOError(f'Hash mismatch: {src} != {dest}')


def move_file(src: str, dest: str, checksum: Optional[bool] = False):
    """Moves a file from the source path to the destination path.

    Args:
        src: The source path.
        dest: The destination path.
        checksum: Whether to validate the checksum of the file.

    Raises:
        IOError: If the checksum is invalid.
    """
    copy_file(src, dest, checksum)
    os.remove(src)
