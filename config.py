"""Configuration for Gritify application."""

import os

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask configuration
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))

# Gridfinity standard dimensions (in mm)
GRIDFINITY_BASE_SIZE = 42.0  # Base grid size
GRIDFINITY_HEIGHT_UNIT = 7.0  # Height unit
GRIDFINITY_TOLERANCE = 0.5  # Tolerance for fit

# Generated files directory
GENERATED_DIR = os.path.join(BASE_DIR, 'generated')
os.makedirs(GENERATED_DIR, exist_ok=True)

# Max dimensions for safety
MAX_GRID_WIDTH = 20
MAX_GRID_DEPTH = 20
MAX_HEIGHT_UNITS = 10
