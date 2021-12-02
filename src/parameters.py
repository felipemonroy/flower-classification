"""
Class for catalog.
"""

from typing import List, Optional

from driconfig import DriConfig
from pydantic import BaseModel


class Download(BaseModel):
    """Model for Download source."""

    url: str
    keep: Optional[bool] = False
    extension: Optional[str] = None
    name: Optional[str] = None

    class Config:
        """Configuring BaseModel."""

        allow_mutation = False


class Split(BaseModel):
    """Model for Splot config."""

    seed: int
    ratio: List[float]

    class Config:
        """Configuring BaseModel."""

        allow_mutation = False


class Parameters(DriConfig):
    """Interface for the parameters.yml file."""

    class Config:
        """Configure the YML file location."""

        config_folder = "./config/parameters"
        config_file_name = "parameters.yml"
        allow_mutation = False

    download_data: Download
    download_labels: Download
    split: Split
