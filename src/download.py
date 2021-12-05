"""
Module with download classes.
"""

import logging
import os
import pathlib
import tarfile
import urllib.request
from typing import Optional

logger = logging.getLogger("default")


def html_download(url: str, destination: str, name: Optional[str] = None) -> str:
    """Download from a html source."""
    # TODO: Add progress bar
    if not name:
        name = url.split("/")[-1]

    logger.info("Downloading file '%s'...", name)

    path = f"{destination}/{name}"
    u = urllib.request.urlopen(url)
    f = open(path, "wb")

    file_size_dl = 0
    block_sz = 8192

    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
    f.close()

    return path


def tgz_extract(
    source: str, destination: str, keep: bool = False, extension: Optional[str] = None
) -> str:
    """Extract files from tgz file."""

    logger.info("Extracting file '%s'...", source)

    with tarfile.open(source, "r:gz") as file:
        for member in file.getmembers():
            if pathlib.Path(member.name).suffix == extension:
                file.extract(member, f"{destination}")

    if not keep:
        os.remove(source)

    return destination
