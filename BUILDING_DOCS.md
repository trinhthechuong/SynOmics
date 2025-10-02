# Building SynOmics Documentation

This document provides instructions for building and viewing the SynOmics documentation.

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

Install the required dependencies:

```bash
pip install -r docs/requirements.txt
```

Or install Sphinx and the theme directly:

```bash
pip install sphinx sphinx-rtd-theme
```

## Building the Documentation

### HTML Documentation

To build the HTML documentation:

```bash
cd docs
make html
```

The generated HTML files will be in `docs/build/html/`. Open `docs/build/html/index.html` in your browser to view.

### PDF Documentation

To build PDF documentation:

```bash
cd docs
make latexpdf
```

### EPUB Documentation

To build EPUB documentation:

```bash
cd docs
make epub
```

### Clean Build

To remove all build artifacts and start fresh:

```bash
cd docs
make clean
```

## Viewing the Documentation Locally

After building, you can serve the documentation locally:

```bash
cd docs/build/html
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Read the Docs Deployment

The documentation is configured for automatic deployment on Read the Docs:

1. The `.readthedocs.yaml` file contains the build configuration
2. Push changes to the repository
3. Read the Docs will automatically build and deploy the documentation

## Documentation Structure

```
docs/
├── Makefile              # Build commands for Unix/Mac
├── make.bat              # Build commands for Windows
├── requirements.txt      # Python dependencies
└── source/
    ├── conf.py          # Sphinx configuration
    ├── index.rst        # Documentation homepage
    ├── usage.rst        # Usage guide
    ├── examples.rst     # Code examples
    ├── api.rst          # API reference
    ├── contributing.rst # Contributing guidelines
    └── changelog.rst    # Version history
```

## Troubleshooting

### Module Import Warnings

If you see warnings about importing the synomics module, this is expected during development. The warnings will not prevent the documentation from building.

### Internet Connection Issues

If you see warnings about intersphinx inventories, this is due to limited internet access. The documentation will still build successfully.

## Contributing to Documentation

When contributing to the documentation:

1. Edit the `.rst` files in `docs/source/`
2. Build the documentation locally to preview changes
3. Ensure there are no build errors
4. Submit a pull request with your changes

For more details, see the [Contributing Guide](docs/source/contributing.rst).
