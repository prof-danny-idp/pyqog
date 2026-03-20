"""Core functionality — read_qog() and helpers."""

from __future__ import annotations

import pandas as pd

from .cache import get_cache_dir, is_cached, read_from_cache
from .urls import build_csv_url, get_cache_filename, _validate_inputs
from .utils import fetch_csv


def read_qog(
    which_data: str = "basic",
    data_type: str = "time-series",
    year: int = 2026,
    data_dir: str | None = None,
    cache: bool = True,
    update_cache: bool = False,
) -> pd.DataFrame:
    """Download (or read from cache) a QoG dataset and return a DataFrame.

    Parameters
    ----------
    which_data : str
        Dataset: "basic", "standard", "oecd", "environmental", "social_policy".
    data_type : str
        "time-series" or "cross-sectional".
    year : int
        Publication year of the dataset (not the data year).
    data_dir : str | None
        Custom cache directory. Default: ``~/.pyqog/cache/``.
    cache : bool
        If True, use local cache when available.
    update_cache : bool
        If True, force re-download even when cache exists.

    Returns
    -------
    pd.DataFrame
    """
    _validate_inputs(which_data, data_type, year)

    cache_dir = get_cache_dir(data_dir)
    filename = get_cache_filename(which_data, data_type, year)

    # Return cached version if available and not forcing update
    if cache and not update_cache and is_cached(cache_dir, filename):
        return read_from_cache(cache_dir, filename)

    # Download and save
    url = build_csv_url(which_data, data_type, year)
    csv_path = fetch_csv(url, cache_dir, filename)
    return pd.read_csv(csv_path, low_memory=False)
