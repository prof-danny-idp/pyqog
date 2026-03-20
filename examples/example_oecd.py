"""Example: Work with the QoG OECD dataset."""

import pyqog

# Download OECD time-series data
print("Downloading QoG OECD time-series dataset...")
df = pyqog.read_qog(which_data="oecd", data_type="time-series")

print(f"Shape: {df.shape}")
print(f"Number of variables: {len(df.columns)}")

# List all available datasets
print("\nAll available datasets:")
datasets = pyqog.list_datasets()
print(datasets[["dataset", "prefix", "n_versions"]])

# List available versions for OECD
versions = pyqog.list_versions("oecd")
print(f"\nAvailable OECD versions: {versions}")

# Get codebook URL
url = pyqog.get_codebook_url("oecd", 2026)
print(f"\nOECD Codebook: {url}")
