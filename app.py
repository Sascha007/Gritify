"""Flask application for Gritify web interface."""

import os
import tempfile
import uuid
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS

from config import (DEBUG, HOST, PORT, GENERATED_DIR, MAX_GRID_WIDTH, MAX_GRID_DEPTH, 
                    MAX_HEIGHT_UNITS, GRIDFINITY_BASE_SIZE, GRIDFINITY_HEIGHT_UNIT, 
                    GRIDFINITY_GRID_BASE_HEIGHT)
from gritify.modules.grid_pattern import GridPattern
from gritify.modules.box import Box
from gritify.modules.inlay_box import InlayBox
from gritify.modules.printbed import PrintbedBreakdown

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)


@app.route('/')
def index():
    """Serve the main page."""
    return send_from_directory('static', 'index.html')


@app.route('/api/generate/grid', methods=['POST'])
def generate_grid():
    """Generate a grid pattern."""
    try:
        data = request.json
        width = int(data.get('width', 1))
        depth = int(data.get('depth', 1))
        include_base = data.get('include_base', True)
        
        # Validate inputs
        if width < 1 or width > MAX_GRID_WIDTH:
            return jsonify({'error': f'Width must be between 1 and {MAX_GRID_WIDTH}'}), 400
        if depth < 1 or depth > MAX_GRID_DEPTH:
            return jsonify({'error': f'Depth must be between 1 and {MAX_GRID_DEPTH}'}), 400
        
        # Generate grid
        grid = GridPattern()
        mesh_obj = grid.generate(width, depth, include_base)
        
        # Save to file
        filename = f'grid_{width}x{depth}_{uuid.uuid4().hex[:8]}.stl'
        filepath = os.path.join(GENERATED_DIR, filename)
        mesh_obj.save(filepath)
        
        # Calculate dimensions
        size_x = width * GRIDFINITY_BASE_SIZE
        size_y = depth * GRIDFINITY_BASE_SIZE
        size_z = GRIDFINITY_GRID_BASE_HEIGHT
        
        return jsonify({
            'success': True,
            'filename': filename,
            'download_url': f'/api/download/{filename}',
            'dimensions': {
                'x': size_x,
                'y': size_y,
                'z': size_z,
                'units': 'mm'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate/box', methods=['POST'])
def generate_box():
    """Generate a box."""
    try:
        data = request.json
        width = int(data.get('width', 1))
        depth = int(data.get('depth', 1))
        height = int(data.get('height', 1))
        wall_thickness = float(data.get('wall_thickness', 2.0))
        
        # Validate inputs
        if width < 1 or width > MAX_GRID_WIDTH:
            return jsonify({'error': f'Width must be between 1 and {MAX_GRID_WIDTH}'}), 400
        if depth < 1 or depth > MAX_GRID_DEPTH:
            return jsonify({'error': f'Depth must be between 1 and {MAX_GRID_DEPTH}'}), 400
        if height < 1 or height > MAX_HEIGHT_UNITS:
            return jsonify({'error': f'Height must be between 1 and {MAX_HEIGHT_UNITS}'}), 400
        
        # Generate box
        box = Box()
        mesh_obj = box.generate(width, depth, height, wall_thickness)
        
        # Save to file
        filename = f'box_{width}x{depth}x{height}_{uuid.uuid4().hex[:8]}.stl'
        filepath = os.path.join(GENERATED_DIR, filename)
        mesh_obj.save(filepath)
        
        # Calculate dimensions
        size_x = width * GRIDFINITY_BASE_SIZE
        size_y = depth * GRIDFINITY_BASE_SIZE
        size_z = height * GRIDFINITY_HEIGHT_UNIT
        
        return jsonify({
            'success': True,
            'filename': filename,
            'download_url': f'/api/download/{filename}',
            'dimensions': {
                'x': size_x,
                'y': size_y,
                'z': size_z,
                'units': 'mm'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate/inlay', methods=['POST'])
def generate_inlay():
    """Generate an inlay box."""
    try:
        data = request.json
        width = int(data.get('width', 1))
        depth = int(data.get('depth', 1))
        height = int(data.get('height', 1))
        divisions_x = int(data.get('divisions_x', 2))
        divisions_y = int(data.get('divisions_y', 2))
        wall_thickness = float(data.get('wall_thickness', 1.5))
        
        # Validate inputs
        if width < 1 or width > MAX_GRID_WIDTH:
            return jsonify({'error': f'Width must be between 1 and {MAX_GRID_WIDTH}'}), 400
        if depth < 1 or depth > MAX_GRID_DEPTH:
            return jsonify({'error': f'Depth must be between 1 and {MAX_GRID_DEPTH}'}), 400
        if height < 1 or height > MAX_HEIGHT_UNITS:
            return jsonify({'error': f'Height must be between 1 and {MAX_HEIGHT_UNITS}'}), 400
        
        # Generate inlay box
        inlay = InlayBox()
        mesh_obj = inlay.generate(width, depth, height, divisions_x, divisions_y, wall_thickness)
        
        # Save to file
        filename = f'inlay_{width}x{depth}x{height}_{uuid.uuid4().hex[:8]}.stl'
        filepath = os.path.join(GENERATED_DIR, filename)
        mesh_obj.save(filepath)
        
        # Calculate dimensions
        size_x = width * GRIDFINITY_BASE_SIZE
        size_y = depth * GRIDFINITY_BASE_SIZE
        size_z = height * GRIDFINITY_HEIGHT_UNIT
        
        return jsonify({
            'success': True,
            'filename': filename,
            'download_url': f'/api/download/{filename}',
            'dimensions': {
                'x': size_x,
                'y': size_y,
                'z': size_z,
                'units': 'mm'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/printbed/calculate', methods=['POST'])
def calculate_printbed():
    """Calculate printbed breakdown."""
    try:
        data = request.json
        total_width = int(data.get('total_width', 1))
        total_depth = int(data.get('total_depth', 1))
        bed_length_x = float(data.get('bed_length_x', 220.0))
        bed_length_y = float(data.get('bed_length_y', 220.0))
        
        # Calculate breakdown
        breakdown = PrintbedBreakdown()
        result = breakdown.calculate_breakdown(total_width, total_depth, bed_length_x, bed_length_y)
        
        return jsonify({
            'success': True,
            'breakdown': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download a generated STL file."""
    try:
        filepath = os.path.join(GENERATED_DIR, filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'Gritify API'})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
