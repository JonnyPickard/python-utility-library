# Python Utility Library

A modular framework for Python-based document processing and utility tools. Built with a locality-of-behavior architecture where each utility module is self-contained with its own inputs, outputs, tests, and scripts.

## Current Utilities

- **PDF to Markdown**: GPU-accelerated conversion using AI models (Marker library)

## Planned Utilities

- **RST to SQL**: Parse reStructuredText documentation and convert to searchable SQL database
- **Document Analysis**: Extract metadata, structure, and content from various document formats
- **Text Processing**: Advanced text manipulation and transformation utilities

## Architecture

Each utility module follows a consistent **locality-of-behavior** pattern:

```txt
python-utility-library/
├── .claude/                      # Claude Code configuration
├── .vscode/                      # VSCode settings and launch configs
├── docs/                         # Documentation and research
├── modules/                      # Utility modules
│   ├── __init__.py
│   └── pdf_to_markdown/          # PDF to Markdown utility
│       ├── __init__.py
│       ├── converter.py          # Core PDFToMarkdownConverter class
│       ├── run_single.py         # Interactive single file conversion
│       ├── run_batch.py          # Interactive batch conversion
│       ├── inputs/               # Input PDFs (gitignored content)
│       │   └── .gitkeep
│       ├── outputs/              # Generated markdown (gitignored content)
│       │   └── .gitkeep
│       └── tests/                # Unit tests with mocking
│           ├── __init__.py
│           └── test_converter.py
├── scripts/                      # Development scripts
│   ├── setup_venv.bat
│   ├── setup_venv.ps1
│   ├── install_deps.bat
│   ├── lint_code.bat
│   └── run_tests.bat
├── venv/                         # Virtual environment (gitignored)
├── CLAUDE.md                     # Development workflow guidance
├── README.md
├── requirements.txt              # Core dependencies
├── requirements-dev.txt          # Development dependencies
├── pyproject.toml                # Project configuration
└── setup.py                     # Package setup

# Future module example:
# └── rst_to_sql/                 # RST documentation parser
#     ├── __init__.py
#     ├── parser.py               # docutils-based RST parsing
#     ├── database.py             # SQL database operations
#     ├── run_convert.py          # Interactive conversion script
#     ├── inputs/                 # RST files (gitignored)
#     ├── outputs/                # SQL dumps (gitignored)
#     └── tests/                  # Unit tests
```

**Key Principles:**

- **Self-contained modules**: Each utility manages its own dependencies, data, and tests
- **Consistent structure**: All modules follow the same organizational pattern
- **Private data**: Input/output directories are gitignored for project-specific content
- **GPU acceleration**: Leverages modern hardware when available

## Setup

1. **Create virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Install in development mode:**

   ```bash
   pip install -e .
   ```

## Usage

### PDF to Markdown Conversion

The `pdf_to_markdown` module provides tools to convert PDF documents to Markdown format using the Marker library.

#### Single File Conversion

```python
from modules.pdf_to_markdown import PDFToMarkdownConverter

converter = PDFToMarkdownConverter()

# Convert a single PDF
output_path = converter.convert_single_file(
    "modules/pdf_to_markdown/inputs/document.pdf",
    "modules/pdf_to_markdown/outputs/document.md"
)
```

#### Batch Folder Conversion

```python
# Convert all PDFs in inputs folder
converted_files = converter.convert_folder(
    "modules/pdf_to_markdown/inputs",
    "modules/pdf_to_markdown/outputs",
    overwrite=False  # Skip existing files
)
```

## Testing

Run tests using pytest:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=modules

# Run specific module tests
pytest modules/pdf_to_markdown/tests/
```

## Dependencies

- **marker-pdf**: Core library for PDF to Markdown conversion
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting

## Development

This project uses:

- Python 3.9+
- pytest for testing
- black for code formatting
- flake8 for linting
- mypy for type checking

### Code Style

Format code with black:

```bash
black modules/
```

Check code with flake8:

```bash
flake8 modules/
```

Type check with mypy:

```bash
mypy modules/
```
