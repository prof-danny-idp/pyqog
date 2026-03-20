# pyqog

[![PyPI version](https://badge.fury.io/py/pyqog.svg)](https://badge.fury.io/py/pyqog)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

> **PT-BR:** Desenvolvido como ferramenta didática para exercícios em sala de aula das disciplinas de **Data Science** do **Professor Danny de Castro** no **IDP – Instituto Brasileiro de Ensino, Desenvolvimento e Pesquisa**. Para dados oficiais: https://www.gu.se/en/quality-government | Contato: danny.soares@idp.edu.br
>
> **EN:** Developed as a teaching tool for classroom exercises in **Data Science** courses by **Professor Danny de Castro** at **IDP – Instituto Brasileiro de Ensino, Desenvolvimento e Pesquisa** (Brazil). For official data: https://www.gu.se/en/quality-government | Contact: danny.soares@idp.edu.br

---

## PT-BR

### O que é o pyqog?

O `pyqog` é um pacote Python que facilita o download, cache e uso dos datasets do **Quality of Government Institute** (Universidade de Gotemburgo). Inspirado no pacote R [`rqog`](https://github.com/rOpenGov/rqog), este pacote permite acessar dados de governança, corrupção, democracia e outros indicadores políticos diretamente no Python.

### Instalação

```bash
pip install pyqog
```

### Uso rápido

```python
import pyqog

# Baixar dados básicos (time-series, versão mais recente)
df = pyqog.read_qog()

# Baixar dados standard cross-sectional
df = pyqog.read_qog(which_data="standard", data_type="cross-sectional")

# Baixar versão antiga (2020)
df = pyqog.read_qog(which_data="basic", year=2020)

# Listar datasets disponíveis
pyqog.list_datasets()

# Ver versões disponíveis
pyqog.list_versions("standard")

# URL do codebook
url = pyqog.get_codebook_url("standard", 2026)

# Buscar variáveis com "corruption" no nome
cols = pyqog.search_variables(df, "corrupt")

# Info do dataset
info = pyqog.describe_dataset("basic")
```

### Datasets disponíveis

| Dataset | Prefixo | Descrição |
|---------|---------|-----------|
| `basic` | bas | Versão menor com indicadores-chave de governança |
| `standard` | std | O dataset QoG mais abrangente |
| `oecd` | oecd | Dados apenas para países membros da OCDE |
| `environmental` | ei | Indicadores de governança ambiental |
| `social_policy` | soc | Indicadores de política social |

### Documentação completa

Acesse: [https://prof-danny-idp.github.io/pyqog/](https://prof-danny-idp.github.io/pyqog/)

---

## EN

### What is pyqog?

`pyqog` is a Python package that makes it easy to download, cache, and use datasets from the **Quality of Government Institute** (University of Gothenburg). Inspired by the R package [`rqog`](https://github.com/rOpenGov/rqog), this package lets you access governance, corruption, democracy, and other political indicators directly in Python.

### Installation

```bash
pip install pyqog
```

### Quick start

```python
import pyqog

# Download basic time-series data (latest version)
df = pyqog.read_qog()

# Download standard cross-sectional data
df = pyqog.read_qog(which_data="standard", data_type="cross-sectional")

# Download an older version (2020)
df = pyqog.read_qog(which_data="basic", year=2020)

# List available datasets
pyqog.list_datasets()

# List available versions
pyqog.list_versions("standard")

# Get codebook URL
url = pyqog.get_codebook_url("standard", 2026)

# Search for variables with "corruption" in the name
cols = pyqog.search_variables(df, "corrupt")

# Get dataset info
info = pyqog.describe_dataset("basic")
```

### Available datasets

| Dataset | Prefix | Description |
|---------|--------|-------------|
| `basic` | bas | Smaller version with key governance indicators |
| `standard` | std | The most comprehensive QoG dataset |
| `oecd` | oecd | Data for OECD member countries only |
| `environmental` | ei | Environmental governance indicators |
| `social_policy` | soc | Social policy indicators |

### Full documentation

Visit: [https://prof-danny-idp.github.io/pyqog/](https://prof-danny-idp.github.io/pyqog/)

---

## Citation / Citação

> Teorell, Jan, et al. 2026. The Quality of Government Standard Dataset, version Jan26. University of Gothenburg: The Quality of Government Institute, https://www.gu.se/en/quality-government

## License / Licença

MIT License. See [LICENSE](LICENSE).
