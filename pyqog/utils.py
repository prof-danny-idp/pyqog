"""Utility functions for pyqog."""

from __future__ import annotations

import io
import os

import pandas as pd
import requests


def download_csv(url: str, timeout: int = 120) -> pd.DataFrame:
    """Download a CSV from *url* and return it as a DataFrame."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ConnectionError(
            f"Failed to download data from {url}: {exc}"
        ) from exc

    return pd.read_csv(io.StringIO(response.text), low_memory=False)


def fetch_csv(url: str, cache_dir: str, filename: str, timeout: int = 120) -> str:
    """Download a CSV from *url*, save it to *cache_dir/filename*, and return the path.

    If the file already exists, returns the path without downloading.
    """
    filepath = os.path.join(cache_dir, filename)
    if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
        return filepath

    os.makedirs(cache_dir, exist_ok=True)
    df = download_csv(url, timeout=timeout)
    df.to_csv(filepath, index=False)
    return filepath
