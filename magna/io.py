import hashlib
import os
import shutil
import tarfile
import urllib
import urllib.request
from typing import Optional

from tqdm import tqdm

from magna.config import CACHE_DIR


def untar(file_path, dir_name):
    """
    Extracts the contents of the tar file at file_path into the directory
    dest_path.
    """
    with tarfile.open(file_path) as tar:
        tar.extractall(dir_name)


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


def md5sum(path: str) -> str:
    block_size = 65536
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()


def download_file(url: str, path: str, md5: Optional[str] = None):
    """Downloads a file to disk with tqdm progress bar."""
    with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=path, reporthook=t.update_to, data=None)
        t.total = t.n

    if md5 and md5 != md5sum(path):
        raise ValueError('Hash mismatch')


def cache_file(srv_path: str, local_name: str) -> str:
    """Copies a remote file to the local machine."""
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    local_path = os.path.join(CACHE_DIR, local_name)
    if not os.path.isfile(local_path):
        shutil.copyfile(srv_path, local_path)
    return local_path
