"""Tests for pyqog.metadata module."""

import pandas as pd
import pytest

from pyqog.metadata import (
    describe_dataset,
    get_codebook_url,
    list_datasets,
    list_versions,
    search_variables,
)


class TestListDatasets:
    def test_returns_dataframe(self):
        result = list_datasets()
        assert isinstance(result, pd.DataFrame)

    def test_has_all_datasets(self):
        result = list_datasets()
        assert len(result) == 5
        assert "basic" in result["dataset"].values
        assert "standard" in result["dataset"].values
        assert "oecd" in result["dataset"].values

    def test_has_expected_columns(self):
        result = list_datasets()
        expected_cols = {"dataset", "prefix", "description", "data_types",
                         "available_years", "n_versions"}
        assert expected_cols.issubset(set(result.columns))


class TestListVersions:
    def test_basic_returns_list(self):
        result = list_versions("basic")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_standard_includes_2026(self):
        result = list_versions("standard")
        assert 2026 in result

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            list_versions("nonexistent")


class TestGetCodebookUrl:
    def test_basic_2026(self):
        url = get_codebook_url("basic", 2026)
        assert "codebook_bas_jan26.pdf" in url
        assert url.startswith("https://")

    def test_standard_2026(self):
        url = get_codebook_url("standard", 2026)
        assert "codebook_std_jan26.pdf" in url

    def test_invalid_dataset_raises(self):
        with pytest.raises(ValueError):
            get_codebook_url("invalid")


class TestSearchVariables:
    def test_finds_matching_columns(self):
        df = pd.DataFrame({"ti_cpi": [1], "vdem_corr": [2], "gdp": [3]})
        result = search_variables(df, "c.rr")
        assert "vdem_corr" in result

    def test_case_insensitive(self):
        df = pd.DataFrame({"GDP_per_cap": [1], "population": [2]})
        result = search_variables(df, "gdp")
        assert "GDP_per_cap" in result

    def test_returns_empty_for_no_match(self):
        df = pd.DataFrame({"a": [1], "b": [2]})
        result = search_variables(df, "zzzzz")
        assert result == []

    def test_regex_pattern(self):
        df = pd.DataFrame({"wdi_gdp": [1], "wdi_pop": [2], "ti_cpi": [3]})
        result = search_variables(df, "^wdi_")
        assert len(result) == 2
        assert "ti_cpi" not in result


class TestDescribeDataset:
    def test_returns_dict(self):
        result = describe_dataset("basic", 2026)
        assert isinstance(result, dict)

    def test_has_expected_keys(self):
        result = describe_dataset("basic", 2026)
        expected_keys = {"dataset", "prefix", "description", "year",
                         "version", "data_types", "codebook_url",
                         "available_years"}
        assert expected_keys == set(result.keys()) or expected_keys.issubset(set(result.keys()))

    def test_basic_2026_values(self):
        result = describe_dataset("basic", 2026)
        assert result["dataset"] == "basic"
        assert result["prefix"] == "bas"
        assert result["year"] == 2026
        assert result["version"] == "jan26"
        assert "codebook_bas_jan26.pdf" in result["codebook_url"]

    def test_invalid_dataset_raises(self):
        with pytest.raises(ValueError):
            describe_dataset("invalid")

    def test_invalid_year_raises(self):
        with pytest.raises(ValueError):
            describe_dataset("basic", 1990)
