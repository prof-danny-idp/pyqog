"""Metadata, listing, and search functions."""

from __future__ import annotations

import re

import pandas as pd

from .urls import (
    AVAILABLE_DATASETS,
    DATA_TYPE_SUFFIX,
    DATASET_PREFIX,
    YEAR_VERSION,
    build_codebook_url,
    list_available_years,
)

# Human-readable descriptions for each dataset
_DATASET_DESCRIPTIONS = {
    "basic": "QoG Basic Dataset — core governance indicators",
    "standard": "QoG Standard Dataset — comprehensive governance data",
    "oecd": "QoG OECD Dataset — governance data for OECD countries",
    "environmental": "QoG Environmental Indicators Dataset",
    "social_policy": "QoG Social Policy Dataset",
}


def list_datasets() -> pd.DataFrame:
    """List all available QoG datasets with descriptions.

    Returns
    -------
    pd.DataFrame
        Columns: dataset, prefix, description, data_types, available_years, n_versions.
    """
    rows = []
    for name in DATASET_PREFIX:
        years = list_available_years(name)
        rows.append(
            {
                "dataset": name,
                "prefix": DATASET_PREFIX[name],
                "description": _DATASET_DESCRIPTIONS.get(name, ""),
                "data_types": list(DATA_TYPE_SUFFIX.keys()),
                "available_years": years,
                "n_versions": len(years),
            }
        )
    return pd.DataFrame(rows)


def list_versions(which_data: str = "basic") -> list[int]:
    """List publication years available for a given dataset.

    Parameters
    ----------
    which_data : str
        Dataset name.

    Returns
    -------
    list[int]
        Sorted list of available years (descending).
    """
    return list_available_years(which_data)


def get_codebook_url(which_data: str = "basic", year: int = 2026) -> str:
    """Return the URL of the codebook PDF."""
    return build_codebook_url(which_data, year)


def search_variables(df: pd.DataFrame, pattern: str) -> list[str]:
    """Search column names in *df* matching *pattern* (case-insensitive regex).

    Parameters
    ----------
    df : pd.DataFrame
        A QoG DataFrame (as returned by ``read_qog()``).
    pattern : str
        Regular expression or substring to match against column names.

    Returns
    -------
    list[str]
        Matching column names.
    """
    regex = re.compile(pattern, re.IGNORECASE)
    return [col for col in df.columns if regex.search(col)]


def describe_dataset(which_data: str = "basic", year: int = 2026) -> dict:
    """Return metadata about a dataset without downloading it.

    Parameters
    ----------
    which_data : str
        Dataset name.
    year : int
        Publication year.

    Returns
    -------
    dict
        Keys: dataset, prefix, year, version, description, data_types,
        codebook_url, available_years.
    """
    if which_data not in DATASET_PREFIX:
        valid = ", ".join(sorted(DATASET_PREFIX.keys()))
        raise ValueError(
            f"Invalid dataset '{which_data}'. Choose from: {valid}"
        )
    if year not in YEAR_VERSION:
        valid = sorted(YEAR_VERSION.keys(), reverse=True)
        raise ValueError(
            f"Invalid year {year}. Available years: {valid}"
        )

    return {
        "dataset": which_data,
        "prefix": DATASET_PREFIX[which_data],
        "year": year,
        "version": YEAR_VERSION[year],
        "description": _DATASET_DESCRIPTIONS.get(which_data, ""),
        "data_types": list(DATA_TYPE_SUFFIX.keys()),
        "codebook_url": build_codebook_url(which_data, year),
        "available_years": list_available_years(which_data),
    }
