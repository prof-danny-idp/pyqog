# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-03-20

### Added
- Initial release of pyqog
- `read_qog()` function to download and load QoG datasets as pandas DataFrames
- Support for Basic, Standard, OECD, Environmental, and Social Policy datasets
- Support for time-series and cross-sectional data types
- Local CSV caching system (~/.pyqog/cache/)
- `list_datasets()` to list all available datasets
- `list_versions()` to list available years for a dataset
- `get_codebook_url()` to get codebook PDF URLs
- `search_variables()` to search column names by pattern
- `describe_dataset()` to get dataset metadata
- Support for dataset versions from 2008 to 2026
- Bilingual documentation site (PT-BR / EN)
