"""Example: Access archived (older) versions of QoG datasets."""

import pyqog

# Download an older version of the basic dataset
print("Downloading QoG Basic time-series dataset (2020 version)...")
df_2020 = pyqog.read_qog(which_data="basic", year=2020)
print(f"2020 version shape: {df_2020.shape}")

# Download the latest version for comparison
print("\nDownloading QoG Basic time-series dataset (2026 version)...")
df_2026 = pyqog.read_qog(which_data="basic", year=2026)
print(f"2026 version shape: {df_2026.shape}")

# Compare number of variables
print(f"\nVariables in 2020: {len(df_2020.columns)}")
print(f"Variables in 2026: {len(df_2026.columns)}")

# List all available versions for basic
versions = pyqog.list_versions("basic")
print(f"\nAll available Basic versions: {versions}")

# Codebook URLs for old vs new
url_old = pyqog.get_codebook_url("basic", 2020)
url_new = pyqog.get_codebook_url("basic", 2026)
print(f"\n2020 Codebook: {url_old}")
print(f"2026 Codebook: {url_new}")
