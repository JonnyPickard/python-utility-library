# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a modular Python utility library focused on PDF to Markdown conversion. The architecture follows locality-of-behavior principles where each module is self-contained.

### Core Structure
- **Modular design**: Each utility module lives in `modules/` with its own inputs, outputs, tests, and scripts
- **Locality principle**: All module-related files (code, tests, data, scripts) are co-located within the module directory
- **Self-contained modules**: Each module can import from other modules but manages its own dependencies and data

### PDF to Markdown Module
The main module uses the Marker library for conversion:
- **PDFToMarkdownConverter class**: Handles single file and batch folder conversions with lazy model loading
- **Input/Output pattern**: PDFs go in `modules/pdf_to_markdown/inputs/`, markdown files are created in `outputs/`
- **Error handling**: Continues processing other files if one conversion fails
- **Unit tests**: Comprehensive mocking of Marker library for testing without actual PDF processing

## Development Commands

### Environment Setup
```bash
# Initial setup (Windows)
scripts\setup_venv.bat
# or PowerShell
scripts\setup_venv.ps1

# Install/update dependencies
scripts\install_deps.bat

# Activate environment manually
venv\Scripts\activate.bat
```

### Testing
```bash
# Run all tests
pytest

# Test specific module
pytest modules/pdf_to_markdown/tests/

# Run with coverage
pytest --cov=modules --cov-report=html

# Via script
scripts\run_tests.bat
```

### Code Quality
```bash
# Format code
black modules/ scripts/

# Lint code
flake8 modules/ scripts/

# Type checking  
mypy modules/

# All quality checks
scripts\lint_code.bat
```

### Running Conversions
```bash
# Single file conversion (interactive)
python modules/pdf_to_markdown/run_single.py

# Batch conversion (interactive)
python modules/pdf_to_markdown/run_batch.py
```

### VSCode Integration
The project includes comprehensive VSCode configuration:
- **Launch configurations**: Run single/batch conversions and tests directly from F5
- **Tasks**: Common operations via Ctrl+Shift+P > Tasks
- **Settings**: Python interpreter, testing, linting, and formatting configured for the virtual environment

## Key Development Patterns

### Module Structure Template
When adding new modules, follow this pattern:
```
modules/new_module/
├── __init__.py          # Module exports
├── core_functionality.py
├── run_single.py        # Interactive single operation
├── run_batch.py         # Interactive batch operation  
├── inputs/              # Input data
├── outputs/             # Generated outputs
└── tests/
    ├── __init__.py
    └── test_*.py
```

### Testing Strategy
- Mock external libraries (like Marker) to avoid heavyweight dependencies in tests
- Use temporary directories for file operations
- Test both success and failure cases
- Test lazy loading and resource management patterns

### Error Handling
- Continue processing remaining items if one fails in batch operations
- Provide clear user feedback about what succeeded/failed
- Log detailed errors for debugging while showing user-friendly messages