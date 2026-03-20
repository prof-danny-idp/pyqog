"""Tests for pyqog.cache module."""

import os
import tempfile

import pytest

from pyqog.cache import (
    clear_cache,
    get_cache_dir,
    get_cache_path,
    is_cached,
)


class TestGetCacheDir:
    def test_default_cache_dir(self):
        cache_dir = get_cache_dir()
        assert cache_dir.endswith(os.path.join(".pyqog", "cache"))
        assert os.path.isdir(cache_dir)

    def test_custom_cache_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            custom = os.path.join(tmpdir, "my_cache")
            result = get_cache_dir(custom)
            assert result == custom
            assert os.path.isdir(custom)


class TestGetCachePath:
    def test_returns_full_path(self):
        path = get_cache_path("/tmp/cache", "test.csv")
        assert path == os.path.join("/tmp/cache", "test.csv")


class TestIsCached:
    def test_returns_false_for_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            assert is_cached(tmpdir, "nonexistent.csv") is False

    def test_returns_false_for_empty_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "empty.csv")
            with open(filepath, "w") as f:
                pass  # create empty file
            assert is_cached(tmpdir, "empty.csv") is False

    def test_returns_true_for_existing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "data.csv")
            with open(filepath, "w") as f:
                f.write("col1,col2\n1,2\n")
            assert is_cached(tmpdir, "data.csv") is True


class TestClearCache:
    def test_removes_csv_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create some CSV files
            for name in ["a.csv", "b.csv", "c.csv"]:
                with open(os.path.join(tmpdir, name), "w") as f:
                    f.write("data")

            count = clear_cache(tmpdir)
            assert count == 3

            remaining = os.listdir(tmpdir)
            assert len(remaining) == 0

    def test_does_not_remove_non_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "readme.txt"), "w") as f:
                f.write("keep me")
            with open(os.path.join(tmpdir, "data.csv"), "w") as f:
                f.write("remove me")

            count = clear_cache(tmpdir)
            assert count == 1
            assert "readme.txt" in os.listdir(tmpdir)

    def test_empty_cache_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            count = clear_cache(tmpdir)
            assert count == 0
