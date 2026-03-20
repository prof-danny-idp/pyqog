"""Example: Download and explore the QoG Basic dataset."""

import pyqog

# Download the basic time-series dataset (latest version)
print("Downloading QoG Basic time-series dataset...")
df = pyqog.read_qog()

print(f"Shape: {df.shape}")
print(f"Columns: {len(df.columns)}")
print(f"\nFirst 5 rows:")
print(df.head())

# Search for corruption-related variables
print("\nVariables containing 'corrupt':")
corrupt_vars = pyqog.search_variables(df, "corrupt")
print(corrupt_vars)

# Dataset info
info = pyqog.describe_dataset("basic")
print(f"\nDataset info: {info}")
