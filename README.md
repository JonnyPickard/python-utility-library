# Python Utility Library

A focused utility library for PDF to Markdown conversion using the Marker library.

## Project Structure

```
python-utility-library/
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── .python-version
├── setup.py
├── pyproject.toml
└── modules/
    └── pdf_to_markdown/
        ├── __init__.py
        ├── converter.py
        ├── inputs/          # Place PDF files here
        ├── outputs/         # Markdown files will be created here
        └── tests/
            ├── __init__.py
            └── test_converter.py
```

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