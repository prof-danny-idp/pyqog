"""URL mapping for QoG datasets."""

# Dataset name -> URL prefix
DATASET_PREFIX = {
    "basic": "bas",
    "standard": "std",
    "oecd": "oecd",
    "environmental": "ei",
    "social_policy": "soc",
}

# Data type -> URL suffix
DATA_TYPE_SUFFIX = {
    "time-series": "ts",
    "cross-sectional": "cs",
}

# Year -> version string
YEAR_VERSION = {
    2026: "jan26",
    2025: "jan25",
    2024: "jan24",
    2023: "jan23",
    2022: "jan22",
    2021: "jan21",
    2020: "jan20",
    2019: "jan19",
    2018: "jan18",
    2017: "jan17",
    2016: "jan16",
    2015: "jan15",
    2014: "jan14",
    2013: "30aug13",
    2012: "21may12",
    2011: "6apr11",
    2010: "27may10",
    2009: "17sep09",
    2008: "15may08",
}

# Which datasets are available for each year
# basic and standard are available for all years; others have limited availability
AVAILABLE_DATASETS = {}
for _y in YEAR_VERSION:
    _ds = ["basic", "standard"]
    if _y >= 2015:
        _ds.append("oecd")
    if _y >= 2017:
        _ds.append("environmental")
    if _y >= 2021:
        _ds.append("social_policy")
    AVAILABLE_DATASETS[_y] = _ds

# The most recent year uses /data/, all others use /dataarchive/
CURRENT_YEAR = 2026

BASE_URL_CURRENT = "https://www.qogdata.pol.gu.se/data/"
BASE_URL_ARCHIVE = "https://www.qogdata.pol.gu.se/dataarchive/"


def get_base_url(year: int) -> str:
    """Return the base URL for a given publication year."""
    return BASE_URL_CURRENT if year == CURRENT_YEAR else BASE_URL_ARCHIVE


def _validate_inputs(which_data: str, data_type: str, year: int) -> None:
    """Validate parameters and raise ValueError if invalid."""
    if which_data not in DATASET_PREFIX:
        valid = ", ".join(sorted(DATASET_PREFIX.keys()))
        raise ValueError(
            f"Invalid dataset '{which_data}'. Choose from: {valid}"
        )
    if data_type not in DATA_TYPE_SUFFIX:
        valid = ", ".join(sorted(DATA_TYPE_SUFFIX.keys()))
        raise ValueError(
            f"Invalid data_type '{data_type}'. Choose from: {valid}"
        )
    if year not in YEAR_VERSION:
        valid = sorted(YEAR_VERSION.keys(), reverse=True)
        raise ValueError(
            f"Invalid year {year}. Available years: {valid}"
        )
    if which_data not in AVAILABLE_DATASETS.get(year, []):
        raise ValueError(
            f"Dataset '{which_data}' is not available for year {year}."
        )


def build_csv_url(
    which_data: str = "basic",
    data_type: str = "time-series",
    year: int = 2026,
) -> str:
    """Build the CSV download URL for a QoG dataset."""
    _validate_inputs(which_data, data_type, year)

    prefix = DATASET_PREFIX[which_data]
    suffix = DATA_TYPE_SUFFIX[data_type]
    version = YEAR_VERSION[year]
    base = get_base_url(year)
    filename = f"qog_{prefix}_{suffix}_{version}.csv"
    return base + filename


# Keep backward-compatible alias
build_data_url = build_csv_url


def build_codebook_url(which_data: str = "basic", year: int = 2026) -> str:
    """Build the codebook PDF URL for a QoG dataset."""
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

    prefix = DATASET_PREFIX[which_data]
    version = YEAR_VERSION[year]
    base = get_base_url(year)
    filename = f"codebook_{prefix}_{version}.pdf"
    return base + filename


def get_cache_filename(
    which_data: str = "basic",
    data_type: str = "time-series",
    year: int = 2026,
) -> str:
    """Return the local cache filename for a dataset."""
    prefix = DATASET_PREFIX[which_data]
    suffix = DATA_TYPE_SUFFIX[data_type]
    version = YEAR_VERSION[year]
    return f"qog_{prefix}_{suffix}_{version}.csv"


def list_available_years(which_data: str = "basic") -> list[int]:
    """Return years available for a given dataset, sorted descending."""
    if which_data not in DATASET_PREFIX:
        valid = ", ".join(sorted(DATASET_PREFIX.keys()))
        raise ValueError(
            f"Invalid dataset '{which_data}'. Choose from: {valid}"
        )
    years = [y for y, ds_list in AVAILABLE_DATASETS.items() if which_data in ds_list]
    return sorted(years, reverse=True)
