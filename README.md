# Gritify

A modular Python web application for generating 3D printable Gridfinity structures with real-time 3D preview in your browser.

## Features

- 🔲 **Grid Pattern Generator** - Create customizable Gridfinity grid patterns
- 📦 **Box Generator** - Generate storage boxes with configurable dimensions
- 🗂️ **Inlay Box Generator** - Create compartmentalized boxes with internal divisions
- 🖨️ **Printbed Calculator** - Calculate how to split large structures to fit your printer bed
- 🎨 **Web Interface** - Modern, intuitive web UI with responsive design
- 📥 **STL Export** - Download generated models as STL files ready for slicing

## Technology Stack

- **Backend**: Flask (Python web framework)
- **3D Geometry**: numpy-stl (STL file generation)
- **Frontend**: HTML5, CSS3, JavaScript
- **3D Preview**: Ready for Three.js integration (requires external CDN access)

## API Endpoints

- `POST /api/generate/grid` - Generate grid pattern
- `POST /api/generate/box` - Generate storage box
- `POST /api/generate/inlay` - Generate inlay box
- `POST /api/printbed/calculate` - Calculate printbed breakdown
- `GET /api/download/<filename>` - Download STL file
- `GET /api/health` - Health check

## License

MIT License - see LICENSE file for details
