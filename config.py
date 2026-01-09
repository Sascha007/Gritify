"""Configuration for Gritify application."""

import os

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask configuration
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
HOST = os.environ.get('HOST', '127.0.0.1')
PORT = int(os.environ.get('PORT', 5020))

# Gridfinity standard dimensions (in mm)
GRID_PITCH = 42.0  # mm, Gridfinity pitch (one cell)
Z_UNIT = 7.0  # mm, vertical unit (not needed for 2D)

# Clearances for bin footprint relative to grid pitch
XY_CLEARANCE_TOTAL = 0.5  # mm total (42 -> 41.5)
XY_CLEARANCE_PER_SIDE = 0.25  # mm per side

# Corner radii (top view)
R_BASEPLATE = 8.0  # mm (baseplate cell outer corners)
R_BIN = 3.75  # mm (bin/block footprint corners)

# Legacy constants (kept for backward compatibility)
GRIDFINITY_BASE_SIZE = 42.0  # Base grid size
GRIDFINITY_HEIGHT_UNIT = 7.0  # Height unit
GRIDFINITY_TOLERANCE = 0.5  # Tolerance for fit
GRIDFINITY_GRID_BASE_HEIGHT = 5.0  # Grid base height

# Generated files directory
GENERATED_DIR = os.path.join(BASE_DIR, 'generated')
os.makedirs(GENERATED_DIR, exist_ok=True)

# Max dimensions for safety
MAX_GRID_WIDTH = 20
MAX_GRID_DEPTH = 20
MAX_HEIGHT_UNITS = 10
