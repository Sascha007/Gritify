# Gritify

A modular Python web application for generating 3D printable Gridfinity structures with real-time 3D preview in your browser.

## Features

- 🔲 **Grid Pattern Generator** - Create customizable Gridfinity grid patterns
- 📦 **Box Generator** - Generate storage boxes with configurable dimensions
- 🗂️ **Inlay Box Generator** - Create compartmentalized boxes with internal divisions
- 🖨️ **Printbed Calculator** - Calculate how to split large structures to fit your printer bed
- 🎨 **Web Interface** - Modern, intuitive web UI with responsive design
- 📥 **STL Export** - Download generated models as STL files ready for slicing

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Sascha007/Gritify.git
cd Gritify
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Simply run:
```bash
python run.py
```

Or use the main app directly:
```bash
python app.py
```

### Using the Web Interface

1. Open your browser and navigate to:
```
http://localhost:5000
```

2. Use the web interface to:
   - Select a component type (Grid, Box, Inlay, or Printbed)
   - Configure dimensions and parameters
   - Click "Generate" to create the 3D model
   - Download the STL file

### Generated Files

All generated STL files are saved in the `generated/` directory with unique filenames.

## Project Structure

```
Gritify/
├── run.py                    # Quick start script
├── app.py                    # Flask web application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── gritify/                  # Core module
│   ├── __init__.py
│   ├── geometry.py           # Base geometry utilities
│   └── modules/              # Modular generators
│       ├── __init__.py
│       ├── grid_pattern.py   # Grid pattern generator
│       ├── box.py            # Box generator
│       ├── inlay_box.py      # Inlay box generator
│       └── printbed.py       # Printbed breakdown calculator
├── static/                   # Web frontend
│   ├── index.html            # Main HTML page
│   └── app.js                # Frontend JavaScript
└── generated/                # Generated STL files (created automatically)
```

## Configuration

Edit `config.py` to customize:

- Server host and port
- Gridfinity dimensions (base size, height unit, tolerance)
- Maximum dimensions for safety
- Generated files directory

## Gridfinity Standard

Gritify follows the Gridfinity standard specifications:
- Base grid size: 42mm
- Height unit: 7mm
- Tolerance: 0.5mm

## Testing

### Running Tests

The project includes comprehensive unit and integration tests with 94% code coverage.

#### Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

#### Run All Tests

```bash
pytest tests/ -v
```

#### Run Tests with Coverage Report

```bash
pytest tests/ -v --cov=gritify --cov=app --cov-report=term --cov-report=html
```

This will generate:
- Terminal coverage report
- HTML coverage report in `htmlcov/` directory

#### Run Specific Test Categories

```bash
# Run only unit tests (modules)
pytest tests/test_geometry.py tests/test_grid_pattern.py tests/test_box.py tests/test_inlay_box.py tests/test_printbed.py -v

# Run only integration tests (API)
pytest tests/test_api.py -v
```

### Test Structure

```
tests/
├── test_geometry.py       # Tests for GridfinityBase class (7 tests)
├── test_grid_pattern.py   # Tests for GridPattern module (7 tests)
├── test_box.py            # Tests for Box module (8 tests)
├── test_inlay_box.py      # Tests for InlayBox module (9 tests)
├── test_printbed.py       # Tests for PrintbedBreakdown module (10 tests)
└── test_api.py            # Integration tests for Flask API (21 tests)
```

**Total: 62 tests with 94% code coverage**

### Continuous Integration

The project uses GitHub Actions for automated testing. Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual workflow dispatch

The CI workflow:
1. Tests against Python 3.8, 3.9, 3.10, 3.11, and 3.12
2. Runs all unit and integration tests
3. Generates code coverage reports
4. Uploads coverage to Codecov (if configured)
5. Comments PR with coverage percentage

## API Endpoints

- `POST /api/generate/grid` - Generate grid pattern
- `POST /api/generate/box` - Generate storage box
- `POST /api/generate/inlay` - Generate inlay box
- `POST /api/printbed/calculate` - Calculate printbed breakdown
- `GET /api/download/<filename>` - Download STL file
- `GET /api/health` - Health check

## License

MIT License - see LICENSE file for details
