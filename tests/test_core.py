"""Tests for pyqog.core module."""

import os
import tempfile
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from pyqog.core import read_qog


class TestReadQog:
    def test_invalid_dataset_raises(self):
        with pytest.raises(ValueError, match="Invalid dataset"):
            read_qog(which_data="invalid")

    def test_invalid_data_type_raises(self):
        with pytest.raises(ValueError, match="Invalid data_type"):
            read_qog(data_type="invalid")

    def test_invalid_year_raises(self):
        with pytest.raises(ValueError, match="Invalid year"):
            read_qog(year=1990)

    def test_read_from_cache(self):
        """Test that read_qog returns a DataFrame from a cached CSV."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a fake cached CSV
            csv_content = "cname,year,ccode\nSweden,2020,752\nBrazil,2020,76\n"
            cache_file = os.path.join(tmpdir, "qog_bas_ts_jan26.csv")
            with open(cache_file, "w") as f:
                f.write(csv_content)

            df = read_qog(
                which_data="basic",
                data_type="time-series",
                year=2026,
                data_dir=tmpdir,
                cache=True,
            )

            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert "cname" in df.columns
            assert "Sweden" in df["cname"].values

    @patch("pyqog.core.fetch_csv")
    def test_read_qog_calls_fetch_csv(self, mock_fetch):
        """Test that read_qog delegates to fetch_csv correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a temp CSV for pandas to read
            csv_path = os.path.join(tmpdir, "test.csv")
            with open(csv_path, "w") as f:
                f.write("col1,col2\n1,2\n")
            mock_fetch.return_value = csv_path

            df = read_qog(
                which_data="basic",
                data_type="time-series",
                year=2026,
                data_dir=tmpdir,
            )

            mock_fetch.assert_called_once()
            call_kwargs = mock_fetch.call_args
            assert "qog_bas_ts_jan26.csv" in str(call_kwargs)

    @patch("pyqog.core.fetch_csv")
    def test_read_qog_standard_cs(self, mock_fetch):
        """Test standard cross-sectional parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            with open(csv_path, "w") as f:
                f.write("cname,ccode\nSweden,752\n")
            mock_fetch.return_value = csv_path

            df = read_qog(
                which_data="standard",
                data_type="cross-sectional",
                year=2025,
            )

            call_kwargs = mock_fetch.call_args
            assert "qog_std_cs_jan25.csv" in str(call_kwargs)

    def test_read_qog_returns_dataframe(self):
        """Test return type with a pre-cached file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_content = "a,b,c\n1,2,3\n4,5,6\n"
            cache_file = os.path.join(tmpdir, "qog_std_ts_jan26.csv")
            with open(cache_file, "w") as f:
                f.write(csv_content)

            result = read_qog(
                which_data="standard",
                data_type="time-series",
                year=2026,
                data_dir=tmpdir,
            )
            assert isinstance(result, pd.DataFrame)
            assert list(result.columns) == ["a", "b", "c"]
