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

## API Endpoints

- `POST /api/generate/grid` - Generate grid pattern
- `POST /api/generate/box` - Generate storage box
- `POST /api/generate/inlay` - Generate inlay box
- `POST /api/printbed/calculate` - Calculate printbed breakdown
- `GET /api/download/<filename>` - Download STL file
- `GET /api/health` - Health check

## License

MIT License - see LICENSE file for details
