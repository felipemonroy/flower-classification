"""
Class for catalog.
"""

from driconfig import DriConfig
from pydantic import BaseModel


class Source(BaseModel):
    """Model for Source."""

    path: str

    class Config:
        """Configuring BaseModel"""

        allow_mutation = False


class Catalog(DriConfig):
    """Interface for the catalog.yml file."""

    class Config:
        """Configure the YML file location."""

        config_folder = "./config/catalog"
        config_file_name = "catalog.yml"
        allow_mutation = False

    raw: Source
    train: Source
    temp: Source
    validation: Source
    test: Source
