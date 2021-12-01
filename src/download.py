"""
Module with download classes.
"""

import os
import pathlib
import tarfile
import urllib.request
from abc import ABC, abstractmethod
from typing import Optional


class Downloader(ABC):
    """Abstract representation of the data downloader."""

    @abstractmethod
    def download(self):
        """Download the data."""
        ...


class Extractor(ABC):
    """Abstract representation of a data extractor."""

    @abstractmethod
    def extract(self):
        """Extract the data."""
        ...


class DataGetter:
    """Context of a data getter with a downloader and an optional extractor."""

    def __init__(self, downloader: Downloader, extractor: Optional[Extractor] = None):
        self.downloader = downloader
        self.extractor = extractor

    def get_data(self):
        """Get the data."""
        self.downloader.download()
        if self.extractor:
            self.extractor.extract()


class HTMLDownloader(Downloader):
    """Download from an html source."""

    def __init__(self, url: str, destination: str, name: Optional[str] = None):
        self.url = url
        self.destination = destination
        if name:
            self.file_name = name
        else:
            self.file_name = self.url.split("/")[-1]

    def download(self):
        """Download the data."""
        u = urllib.request.urlopen(self.url)
        f = open(self.path, "wb")

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
        f.close()

    @property
    def path(self):
        """Get the path of the destination file."""
        return f"{self.destination}/{self.file_name}"


class TGZExtractor(Extractor):
    """Extract the data from a tar gz file."""

    def __init__(
        self,
        source: str,
        destination: str,
        keep: bool = False,
        extension: Optional[str] = None,
    ):
        self.source = source
        self.destination = destination
        self.keep = keep
        self.extension = extension

    def extract(self):
        """Extract the data."""
        with tarfile.open(self.source, "r:gz") as file:
            for member in file.getmembers():
                if pathlib.Path(member.name).suffix == self.extension:
                    file.extract(member, f"{self.destination}")

        if not self.keep:
            os.remove(self.source)
