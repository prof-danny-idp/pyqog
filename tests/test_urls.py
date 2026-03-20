"""Tests for pyqog.urls module."""

import pytest

from pyqog.urls import (
    AVAILABLE_DATASETS,
    CURRENT_YEAR,
    DATASET_PREFIX,
    YEAR_VERSION,
    build_codebook_url,
    build_csv_url,
    get_base_url,
    get_cache_filename,
    list_available_years,
)


class TestGetBaseUrl:
    def test_current_year_returns_current_url(self):
        url = get_base_url(CURRENT_YEAR)
        assert url == "https://www.qogdata.pol.gu.se/data/"

    def test_archive_year_returns_archive_url(self):
        url = get_base_url(2020)
        assert url == "https://www.qogdata.pol.gu.se/dataarchive/"

    def test_all_non_current_years_return_archive(self):
        for year in YEAR_VERSION:
            if year != CURRENT_YEAR:
                assert "dataarchive" in get_base_url(year)


class TestBuildCsvUrl:
    def test_basic_ts_current(self):
        url = build_csv_url("basic", "time-series", 2026)
        assert url == "https://www.qogdata.pol.gu.se/data/qog_bas_ts_jan26.csv"

    def test_standard_cs_current(self):
        url = build_csv_url("standard", "cross-sectional", 2026)
        assert url == "https://www.qogdata.pol.gu.se/data/qog_std_cs_jan26.csv"

    def test_oecd_ts_archive(self):
        url = build_csv_url("oecd", "time-series", 2024)
        assert url == "https://www.qogdata.pol.gu.se/dataarchive/qog_oecd_ts_jan24.csv"

    def test_basic_ts_2013_special_format(self):
        url = build_csv_url("basic", "time-series", 2013)
        assert url == "https://www.qogdata.pol.gu.se/dataarchive/qog_bas_ts_30aug13.csv"

    def test_basic_ts_2012_special_format(self):
        url = build_csv_url("basic", "time-series", 2012)
        assert url == "https://www.qogdata.pol.gu.se/dataarchive/qog_bas_ts_21may12.csv"

    def test_standard_cs_2020(self):
        url = build_csv_url("standard", "cross-sectional", 2020)
        assert url == "https://www.qogdata.pol.gu.se/dataarchive/qog_std_cs_jan20.csv"

    def test_environmental_ts_2019(self):
        url = build_csv_url("environmental", "time-series", 2019)
        assert url == "https://www.qogdata.pol.gu.se/dataarchive/qog_ei_ts_jan19.csv"

    def test_social_policy_2023(self):
        url = build_csv_url("social_policy", "time-series", 2023)
        assert url == "https://www.qogdata.pol.gu.se/dataarchive/qog_soc_ts_jan23.csv"

    def test_invalid_dataset_raises(self):
        with pytest.raises(ValueError, match="Invalid dataset"):
            build_csv_url("invalid", "time-series", 2026)

    def test_invalid_data_type_raises(self):
        with pytest.raises(ValueError, match="Invalid data_type"):
            build_csv_url("basic", "invalid", 2026)

    def test_invalid_year_raises(self):
        with pytest.raises(ValueError, match="Invalid year"):
            build_csv_url("basic", "time-series", 1990)

    def test_dataset_not_available_for_year_raises(self):
        with pytest.raises(ValueError, match="not available for year"):
            build_csv_url("social_policy", "time-series", 2010)

    def test_all_urls_end_with_csv(self):
        for year, datasets in AVAILABLE_DATASETS.items():
            for ds in datasets:
                for dt in ["time-series", "cross-sectional"]:
                    url = build_csv_url(ds, dt, year)
                    assert url.endswith(".csv"), f"URL does not end with .csv: {url}"

    def test_no_dta_in_urls(self):
        for year, datasets in AVAILABLE_DATASETS.items():
            for ds in datasets:
                for dt in ["time-series", "cross-sectional"]:
                    url = build_csv_url(ds, dt, year)
                    assert ".dta" not in url, f"URL contains .dta: {url}"


class TestBuildCodebookUrl:
    def test_basic_current(self):
        url = build_codebook_url("basic", 2026)
        assert url == "https://www.qogdata.pol.gu.se/data/codebook_bas_jan26.pdf"

    def test_standard_current(self):
        url = build_codebook_url("standard", 2026)
        assert url == "https://www.qogdata.pol.gu.se/data/codebook_std_jan26.pdf"

    def test_oecd_current(self):
        url = build_codebook_url("oecd", 2026)
        assert url == "https://www.qogdata.pol.gu.se/data/codebook_oecd_jan26.pdf"

    def test_archive_codebook(self):
        url = build_codebook_url("standard", 2024)
        assert url == "https://www.qogdata.pol.gu.se/dataarchive/codebook_std_jan24.pdf"

    def test_all_codebooks_end_with_pdf(self):
        for year in YEAR_VERSION:
            for ds in DATASET_PREFIX:
                url = build_codebook_url(ds, year)
                assert url.endswith(".pdf")

    def test_invalid_dataset_raises(self):
        with pytest.raises(ValueError, match="Invalid dataset"):
            build_codebook_url("invalid", 2026)

    def test_invalid_year_raises(self):
        with pytest.raises(ValueError, match="Invalid year"):
            build_codebook_url("basic", 1990)


class TestGetCacheFilename:
    def test_basic_ts_2026(self):
        name = get_cache_filename("basic", "time-series", 2026)
        assert name == "qog_bas_ts_jan26.csv"

    def test_standard_cs_2020(self):
        name = get_cache_filename("standard", "cross-sectional", 2020)
        assert name == "qog_std_cs_jan20.csv"

    def test_all_filenames_end_with_csv(self):
        for year, datasets in AVAILABLE_DATASETS.items():
            for ds in datasets:
                for dt in ["time-series", "cross-sectional"]:
                    name = get_cache_filename(ds, dt, year)
                    assert name.endswith(".csv")


class TestListAvailableYears:
    def test_basic_has_all_years(self):
        years = list_available_years("basic")
        assert 2026 in years
        assert 2008 in years
        assert len(years) == len(YEAR_VERSION)

    def test_social_policy_starts_2021(self):
        years = list_available_years("social_policy")
        assert 2021 in years
        assert 2019 not in years

    def test_years_sorted_descending(self):
        years = list_available_years("standard")
        assert years == sorted(years, reverse=True)

    def test_invalid_dataset_raises(self):
        with pytest.raises(ValueError, match="Invalid dataset"):
            list_available_years("invalid")
