# CLAUDE.md — Projeto `pyqog`: Pacote Python para dados QoG

## Visão Geral do Projeto

Criar um pacote Python completo chamado **`pyqog`** publicável no PyPI que replique e expanda as funcionalidades do pacote R `rqog` (https://github.com/rOpenGov/rqog). O pacote baixa, armazena em cache e disponibiliza os datasets do **Quality of Government Institute** (Universidade de Gotemburgo). Além disso, criar um site GitHub Pages bilíngue (PT-BR / EN) para documentação.

## ⚠️ REGRAS ABSOLUTAS

- **NUNCA usar formato .dta (Stata)**. Sempre usar CSV como formato de dados.
- Todos os downloads devem ser CSV compactados ou CSV direto do servidor QoG.
- O pacote deve funcionar offline com cache local após o primeiro download.

---

## 1. ESTRUTURA DO REPOSITÓRIO

```
pyqog/
├── pyqog/
│   ├── __init__.py              # Exporta read_qog, list_datasets, search_metadata, get_codebook_url
│   ├── core.py                  # Função principal read_qog()
│   ├── metadata.py              # Funções de metadata e busca de indicadores
│   ├── urls.py                  # Mapeamento completo de URLs (current + archive)
│   ├── cache.py                 # Sistema de cache local
│   └── utils.py                 # Funções auxiliares
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_urls.py
│   ├── test_metadata.py
│   └── test_cache.py
├── docs/                        # Site GitHub Pages (bilíngue PT/EN)
│   ├── index.html               # Landing page com language switcher
│   ├── pt/
│   │   ├── index.html           # Página principal em português
│   │   ├── instalacao.html
│   │   ├── tutorial.html
│   │   ├── api.html
│   │   └── datasets.html
│   ├── en/
│   │   ├── index.html           # Main page in English
│   │   ├── installation.html
│   │   ├── tutorial.html
│   │   ├── api.html
│   │   └── datasets.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── lang-switcher.js     # Script para alternar PT/EN
├── examples/
│   ├── example_basic.py
│   ├── example_standard.py
│   ├── example_oecd.py
│   └── example_archive.py
├── pyproject.toml
├── setup.cfg
├── README.md                    # Bilíngue PT/EN
├── LICENSE                      # MIT
├── CHANGELOG.md
└── .github/
    └── workflows/
        └── publish.yml          # CI/CD para PyPI
```

---

## 2. PACOTE PYTHON (`pyqog/`)

### 2.1 Função principal: `read_qog()`

```python
def read_qog(
    which_data: str = "basic",       # "basic", "standard", "oecd", "environmental", "social_policy"
    data_type: str = "time-series",  # "time-series" ou "cross-sectional"
    year: int = 2026,                # Ano de publicação do dataset (NÃO ano dos dados)
    data_dir: str | None = None,     # Diretório de cache (None = ~/.pyqog/cache)
    cache: bool = True,              # Usar cache local
    update_cache: bool = False       # Forçar re-download
) -> pd.DataFrame:
```

### 2.2 URLs dos Dados — MAPEAMENTO COMPLETO

**Dados ATUAIS (versão mais recente):**
- Base URL: `https://www.qogdata.pol.gu.se/data/`
- Padrão: `qog_{dataset}_{type}_{version}.csv`
- Exemplo: `https://www.qogdata.pol.gu.se/data/qog_std_cs_jan26.csv`

**Dados ARQUIVADOS (versões anteriores):**
- Base URL: `https://www.qogdata.pol.gu.se/dataarchive/`
- Padrão: `qog_{dataset}_{type}_{version}.csv`
- Exemplo: `https://www.qogdata.pol.gu.se/dataarchive/qog_bas_ts_jan25.csv`

**Mapeamento dataset → prefixo:**
- `basic` → `bas`
- `standard` → `std`
- `oecd` → `oecd`
- `environmental` → `ei`  (se disponível, verificar)
- `social_policy` → `soc`

**Mapeamento data_type → sufixo:**
- `time-series` → `ts`
- `cross-sectional` → `cs`

**Mapeamento year → version string:**
- 2026 → `jan26` (CURRENT — usar base URL `/data/`)
- 2025 → `jan25` (ARCHIVE — usar base URL `/dataarchive/`)
- 2024 → `jan24`
- 2023 → `jan23`
- 2022 → `jan22`
- 2021 → `jan21`
- 2020 → `jan20`
- 2019 → `jan19`
- 2018 → `jan18`
- 2017 → `jan17`
- 2016 → `jan16`
- 2015 → `jan15`
- Versões mais antigas têm formatos diferentes (30aug13, 21may12, etc.) — mapear individualmente

**URLs dos Codebooks (PDF):**
- Current: `https://www.qogdata.pol.gu.se/data/codebook_{dataset}_{version}.pdf`
  - Ex: `https://www.qogdata.pol.gu.se/data/codebook_std_jan26.pdf`
- Archive: `https://www.qogdata.pol.gu.se/dataarchive/codebook_{dataset}_{version}.pdf`
  - Versões antigas podem ter padrões diferentes como `qog_bas_jan23.pdf` ou `codebook_bas_jan25.pdf`

### 2.3 Funções auxiliares

```python
def list_datasets() -> pd.DataFrame:
    """Lista todos os datasets disponíveis com descrição."""

def list_versions(which_data: str = "basic") -> list[int]:
    """Lista anos disponíveis para um dataset."""

def get_codebook_url(which_data: str = "basic", year: int = 2026) -> str:
    """Retorna URL do codebook PDF."""

def search_variables(df: pd.DataFrame, pattern: str) -> list[str]:
    """Busca variáveis por padrão no nome das colunas."""

def describe_dataset(which_data: str = "basic", year: int = 2026) -> dict:
    """Info sobre o dataset: n_vars, n_countries, n_years, etc."""
```

### 2.4 Sistema de Cache

- Diretório padrão: `~/.pyqog/cache/`
- Estrutura: `~/.pyqog/cache/qog_{dataset}_{type}_{version}.csv`
- Se `cache=True` e arquivo existe, não re-baixa
- Se `update_cache=True`, força re-download
- `data_dir` sobrescreve diretório padrão

### 2.5 Dependências

```
pandas>=1.5.0
requests>=2.28.0
```

Apenas essas duas. Manter minimalista.

---

## 3. TESTES (`tests/`)

Usar `pytest`. Testar:
- Construção correta de URLs para todos os datasets/years
- Cache: salvar e ler do disco
- Função `read_qog` com mock (sem download real)
- `list_datasets`, `list_versions`
- `search_variables`
- Tratamento de erros: dataset inválido, ano inválido, sem internet

---

## 4. SITE GITHUB PAGES (`docs/`)

### 4.1 Design

- HTML/CSS/JS puro (sem framework pesado — pode usar Bootstrap CDN)
- Visual profissional, limpo, acadêmico
- Cores: inspirar-se no site QoG (azul escuro, branco, cinza)
- Responsivo (mobile-friendly)

### 4.2 Language Switcher (OBRIGATÓRIO)

- Botão toggle visível no header: 🇧🇷 PT | 🇬🇧 EN
- Ao clicar, redireciona para a versão equivalente no outro idioma
- Manter a URL path structure paralela: `/pt/tutorial.html` ↔ `/en/tutorial.html`
- Salvar preferência em localStorage

### 4.3 AVISO INSTITUCIONAL (OBRIGATÓRIO EM TODAS AS PÁGINAS)

Todas as páginas do site devem conter um **banner/card de destaque** (visível, estilizado, não um rodapé escondido) com o seguinte conteúdo:

**Versão PT-BR:**
> 📚 **Sobre este pacote**
>
> O `pyqog` foi desenvolvido como ferramenta didática para exercícios em sala de aula das disciplinas de **Data Science** do **Professor Danny de Castro** no **IDP – Instituto Brasileiro de Ensino, Desenvolvimento e Pesquisa**.
>
> Este pacote facilita o acesso aos dados do Quality of Government Institute para fins educacionais e de pesquisa acadêmica. **Para uso de dados oficiais e como fonte de informação oficial, acesse diretamente o site do QoG Institute:**
>
> 🔗 [https://www.gu.se/en/quality-government](https://www.gu.se/en/quality-government)
>
> Encontrou algum erro ou tem sugestões? Entre em contato: **danny.soares@idp.edu.br**

**Versão EN:**
> 📚 **About this package**
>
> `pyqog` was developed as a teaching tool for classroom exercises in **Data Science** courses taught by **Professor Danny de Castro** at **IDP – Instituto Brasileiro de Ensino, Desenvolvimento e Pesquisa** (Brazil).
>
> This package facilitates access to Quality of Government Institute data for educational and academic research purposes. **For official data and authoritative information, please access the QoG Institute website directly:**
>
> 🔗 [https://www.gu.se/en/quality-government](https://www.gu.se/en/quality-government)
>
> Found a bug or have suggestions? Contact: **danny.soares@idp.edu.br**

**Implementação:**
- Esse aviso deve aparecer como um card/banner estilizado (com borda, fundo suave azul-claro ou cinza, ícone de livro) na **página inicial** de forma proeminente (hero section ou logo abaixo do hero).
- Nas demais páginas, incluir uma versão compacta no **footer** com o texto resumido e o link para o QoG oficial + email de contato.
- No `README.md` do repositório, incluir este aviso na seção "Sobre / About".

### 4.4 Páginas obrigatórias (em AMBOS os idiomas)

#### Página inicial (`index.html`)
- **Banner institucional** (descrito acima) em destaque
- O que é o QoG
- O que é o pyqog
- Quick start (pip install + código mínimo)
- Links para todas as seções

#### Instalação
- `pip install pyqog`
- Requisitos
- Instalação de desenvolvimento

#### Tutorial Completo
- Baixar dados Basic, Standard, OECD
- Filtrar por país e ano
- Exemplos com matplotlib/seaborn para plots
- Trabalhar com dados cross-sectional vs time-series
- Acessar dados de arquivo (versões antigas)
- Buscar variáveis
- Exemplos reproduzindo os do tutorial R do rqog

#### Referência da API
- Documentação de cada função com parâmetros, retorno, exemplos
- `read_qog()`, `list_datasets()`, `list_versions()`, `get_codebook_url()`, `search_variables()`, `describe_dataset()`

#### Datasets Disponíveis
- Tabela com todos os datasets
- Descrição de cada um
- Número de variáveis e países
- **Links diretos para os PDFs dos codebooks** para TODAS as versões:
  - Basic: https://www.qogdata.pol.gu.se/data/codebook_bas_jan26.pdf (current)
  - Standard: https://www.qogdata.pol.gu.se/data/codebook_std_jan26.pdf (current)
  - OECD: https://www.qogdata.pol.gu.se/data/codebook_oecd_jan26.pdf (current)
  - E links para codebooks antigos no archive
- Link para o Data Finder: https://datafinder.qog.gu.se/
- Link para a página de downloads: https://www.gu.se/en/quality-government/qog-data/data-downloads
- Link para o Data Archive: https://www.gu.se/en/quality-government/qog-data/data-downloads/data-archive

---

## 5. `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "pyqog"
version = "0.1.0"
description = "Python client for Quality of Government (QoG) Institute data"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
authors = [
    {name = "Seu Nome", email = "seu@email.com"}
]
keywords = ["qog", "quality-of-government", "political-science", "open-data", "governance"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering",
]
dependencies = [
    "pandas>=1.5.0",
    "requests>=2.28.0",
]

[project.urls]
Homepage = "https://USERNAME.github.io/pyqog/"
Repository = "https://github.com/USERNAME/pyqog"
Documentation = "https://USERNAME.github.io/pyqog/"
"Bug Tracker" = "https://github.com/USERNAME/pyqog/issues"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

---

## 6. README.md

Bilíngue (PT-BR primeiro, depois EN). Incluir:
- Badges (PyPI version, Python version, License)
- **Aviso institucional** (logo no início, após badges):
  - PT: "Desenvolvido para exercícios em sala de aula das disciplinas de Data Science do Professor Danny de Castro, IDP. Para dados oficiais: https://www.gu.se/en/quality-government | Contato: danny.soares@idp.edu.br"
  - EN: "Developed for classroom exercises in Data Science courses by Professor Danny de Castro, IDP (Brazil). For official data: https://www.gu.se/en/quality-government | Contact: danny.soares@idp.edu.br"
- Descrição
- Instalação rápida
- Exemplo mínimo
- Link para documentação completa
- Citação do QoG
- Licença

---

## 7. EXEMPLOS DE CÓDIGO QUE DEVEM FUNCIONAR

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

---

## 8. CITAÇÃO QoG (incluir no README e no site)

> Teorell, Jan, et al. 2026. The Quality of Government Standard Dataset, version Jan26. University of Gothenburg: The Quality of Government Institute, https://www.gu.se/en/quality-government

---

## 9. ORDEM DE EXECUÇÃO

1. Criar estrutura de diretórios
2. Implementar `pyqog/urls.py` com mapeamento completo de URLs
3. Implementar `pyqog/cache.py`
4. Implementar `pyqog/core.py` com `read_qog()`
5. Implementar `pyqog/metadata.py`
6. Implementar `pyqog/__init__.py` com exports
7. Criar `pyproject.toml`, `setup.cfg`, `LICENSE`, `README.md`
8. Escrever testes em `tests/`
9. Criar exemplos em `examples/`
10. Criar site docs/ com HTML/CSS/JS bilíngue
11. Rodar testes
12. Verificar que tudo está integrado

---

## 10. LINKS IMPORTANTES PARA REFERÊNCIA

- Tutorial R rqog: https://ropengov.github.io/rqog/articles/rqog_tutorial.html
- GitHub rqog: https://github.com/rOpenGov/rqog
- QoG Data Downloads: https://www.gu.se/en/quality-government/qog-data/data-downloads
- QoG Data Archive: https://www.gu.se/en/quality-government/qog-data/data-downloads/data-archive
- QoG Data Finder: https://datafinder.qog.gu.se/
- Codebook Standard Jan26: https://www.qogdata.pol.gu.se/data/codebook_std_jan26.pdf
- Codebook Basic Jan26: https://www.qogdata.pol.gu.se/data/codebook_bas_jan26.pdf  
- Codebook OECD Jan26: https://www.qogdata.pol.gu.se/data/codebook_oecd_jan26.pdf
