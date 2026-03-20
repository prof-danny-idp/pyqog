"""Local cache system for QoG datasets."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

DEFAULT_CACHE_DIR = os.path.join(Path.home(), ".pyqog", "cache")


def get_cache_dir(data_dir: str | None = None) -> str:
    """Return the cache directory, creating it if needed."""
    cache_dir = data_dir if data_dir else DEFAULT_CACHE_DIR
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def get_cache_path(cache_dir: str, filename: str) -> str:
    """Return the full path for a cached file."""
    return os.path.join(cache_dir, filename)


def is_cached(cache_dir: str, filename: str) -> bool:
    """Check if a non-empty file exists in the cache."""
    path = get_cache_path(cache_dir, filename)
    return os.path.isfile(path) and os.path.getsize(path) > 0


def read_from_cache(cache_dir: str, filename: str) -> pd.DataFrame:
    """Read a cached CSV file as a DataFrame."""
    path = get_cache_path(cache_dir, filename)
    return pd.read_csv(path, low_memory=False)


def save_to_cache(
    df: pd.DataFrame, cache_dir: str, filename: str
) -> str:
    """Save a DataFrame to the cache as CSV. Returns the file path."""
    os.makedirs(cache_dir, exist_ok=True)
    path = get_cache_path(cache_dir, filename)
    df.to_csv(path, index=False)
    return path


def clear_cache(cache_dir: str | None = None) -> int:
    """Remove all CSV files from the cache directory.

    Returns the number of files removed.
    """
    cache_dir = cache_dir if cache_dir else DEFAULT_CACHE_DIR
    if not os.path.isdir(cache_dir):
        return 0
    count = 0
    for f in os.listdir(cache_dir):
        if f.endswith(".csv"):
            os.remove(os.path.join(cache_dir, f))
            count += 1
    return count
