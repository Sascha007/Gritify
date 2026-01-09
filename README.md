# Gritify

A modular Python web application for generating 3D printable Gridfinity structures with real-time 3D preview in your browser.

## Features

- 🔲 **Grid Pattern Generator** - Create customizable Gridfinity grid patterns
- 📦 **Box Generator** - Generate storage boxes with configurable dimensions
- 🗂️ **Inlay Box Generator** - Create compartmentalized boxes with internal divisions
- 🖨️ **Printbed Calculator** - Calculate how to split large structures to fit your printer bed
- 🎨 **3D Preview** - Real-time 3D rendering in the browser using Three.js
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

1. Start the web server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Use the web interface to:
   - Select a component type (Grid, Box, Inlay, or Printbed)
   - Configure dimensions and parameters
   - Click "Generate" to create the 3D model
   - Preview the model in the 3D viewer
   - Download the STL file

## Project Structure

```
Gritify/
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
└── static/                   # Web frontend
    ├── index.html            # Main HTML page
    └── app.js                # Frontend JavaScript

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

## Technology Stack

- **Backend**: Flask (Python web framework)
- **3D Geometry**: numpy-stl (STL file generation)
- **Frontend**: HTML5, CSS3, JavaScript
- **3D Rendering**: Three.js (WebGL-based 3D library)

## API Endpoints

- `POST /api/generate/grid` - Generate grid pattern
- `POST /api/generate/box` - Generate storage box
- `POST /api/generate/inlay` - Generate inlay box
- `POST /api/printbed/calculate` - Calculate printbed breakdown
- `GET /api/download/<filename>` - Download STL file
- `GET /api/health` - Health check

## License

MIT License - see LICENSE file for details
