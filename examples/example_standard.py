"""Example: Work with the QoG Standard dataset."""

import pyqog

# Download standard cross-sectional data
print("Downloading QoG Standard cross-sectional dataset...")
df = pyqog.read_qog(which_data="standard", data_type="cross-sectional")

print(f"Shape: {df.shape}")
print(f"Number of variables: {len(df.columns)}")

# Search for GDP-related variables
gdp_vars = pyqog.search_variables(df, "gdp")
print(f"\nGDP-related variables: {gdp_vars}")

# Search for democracy-related variables
dem_vars = pyqog.search_variables(df, "dem")
print(f"\nDemocracy-related variables ({len(dem_vars)} found):")
for v in dem_vars[:10]:
    print(f"  - {v}")

# Get codebook URL for more information
url = pyqog.get_codebook_url("standard", 2026)
print(f"\nCodebook PDF: {url}")
