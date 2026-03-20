"""pyqog — Python client for Quality of Government (QoG) Institute data."""

from .core import read_qog
from .metadata import (
    describe_dataset,
    get_codebook_url,
    list_datasets,
    list_versions,
    search_variables,
)

__version__ = "0.1.0"

__all__ = [
    "read_qog",
    "list_datasets",
    "list_versions",
    "get_codebook_url",
    "search_variables",
    "describe_dataset",
]
