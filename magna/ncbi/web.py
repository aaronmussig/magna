import os
import re
import tempfile
import urllib
import urllib.request
from enum import Enum
from typing import Dict, Tuple
from urllib.parse import urljoin

from magna.ncbi.accession import is_valid_ncbi_gid
from magna.util.disk import move_file
from magna.util.web import download_file


def get_ncbi_assembly_id(gid: str) -> str:
    """Return the assembly ID for a given NCBI accession.

    Args:
        gid: The NCBI accession.

    Returns:
        The NCBI assembly.

    Examples:
        >>> get_ncbi_assembly_id('GCA_003138775.1')
        'GCA_003138775.1_20110800_S2D'
    """
    if not is_valid_ncbi_gid(gid):
        raise ValueError(f'Invalid NCBI accession: {gid}')
    base = 'https://ftp.ncbi.nlm.nih.gov/genomes/all/'
    url = urljoin(base, f'{gid[0:3]}/{gid[4:7]}/{gid[7:10]}/{gid[10:13]}')

    urlpath = urllib.request.urlopen(url)
    string = urlpath.read().decode('utf-8')
    hits = re.findall(f'<a href="({gid}.+)/">', string)
    if len(hits) == 0:
        raise Exception(f'No hits found: {url}')
    if len(hits) > 1:
        raise NotImplemented(f'Found multiple hits: {hits}')
    if not hits[0].startswith(gid):
        raise Exception(f'No gid found: {url}')
    return hits[0]


def get_ncbi_ftp_root(gid: str) -> Tuple[str, str]:
    """Return the FTP root and assembly ID for a given NCBI accession.

    Args:
        gid: The NCBI accession.

    Returns:
        The FTP root and assembly ID.

    Examples:
        >>> get_ncbi_ftp_root('GCA_003138775.1')
        ('https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/138/775/GCA_003138775.1_20110800_S2D/', 'GCA_003138775.1_20110800_S2D')
    """
    assembly = get_ncbi_assembly_id(gid)
    base = 'https://ftp.ncbi.nlm.nih.gov/genomes/all/'
    url = urljoin(base, f'{gid[0:3]}/{gid[4:7]}/{gid[7:10]}/{gid[10:13]}/{assembly}/')
    return url, assembly


def get_md5checksums(url: str) -> Dict[str, str]:
    """Retrieve the md5checksums.txt file and parse the content.

    Args:
        url: The URL to the md5checksums.txt file.

    Returns:
        A dictionary of md5checksums.

    Examples:
        >>> get_md5checksums('https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/138/775/GCA_003138775.1_20110800_S2D/md5checksums.txt')
        {'GCA_003138775.1_20110800_S2D.fna.gz': 'f9f8f8f8f8f8f8f8f8f8f8f8f8f8f8', ...}
    """
    out = dict()
    urlpath = urllib.request.urlopen(url)
    for line in urlpath.read().decode('utf-8').splitlines():
        md5, file = line.split()
        if file.startswith('./'):
            file = file[2:]
        out[file] = md5
    return out


class NcbiAssemblyFileType(str, Enum):
    fna = 'fna'


def download_ncbi_assembly_file_to_disk(gid: str, target: str, file: NcbiAssemblyFileType, silent: bool = False):
    """Download a file from the NCBI assembly directory to disk.

    Args:
        gid: The NCBI accession.
        target: The target path.
        file: The file type to download.
        silent: True if the progress should be hidden.

    Examples:
        >>> download_ncbi_assembly_file_to_disk('GCA_003138775.1', '/tmp/foo.fna.gz', NcbiAssemblyFileType.fna)
    """
    # Create the directory if it doesn't exist
    if os.path.isfile(target):
        return
    else:
        os.makedirs(os.path.dirname(target), exist_ok=True)

    # Generate the paths
    root, assembly = get_ncbi_ftp_root(gid)
    md5s = get_md5checksums(urljoin(root, 'md5checksums.txt'))
    if file == NcbiAssemblyFileType.fna:
        name = f'{assembly}_genomic.fna.gz'
        url = urljoin(root, name)
        md5 = md5s[name]
    else:
        raise NotImplementedError(f'File type not implemented: {file}')

    # Download to a temporary location and verify the md5
    with tempfile.TemporaryDirectory() as tmpdir:
        target_tmp = os.path.join(tmpdir, name)
        download_file(url, target_tmp, md5, silent=silent)
        move_file(target_tmp, target, checksum=True)
