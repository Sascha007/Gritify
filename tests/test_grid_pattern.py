"""Unit tests for grid_pattern module."""

import pytest
import numpy as np
from gritify.modules.grid_pattern import GridPattern


class TestGridPattern:
    """Test cases for GridPattern class."""
    
    def test_init(self):
        """Test GridPattern initialization."""
        grid = GridPattern()
        assert grid.base_size == 42.0
        assert grid.height_unit == 7.0
        assert grid.tolerance == 0.5
    
    def test_generate_1x1_with_base(self):
        """Test generating 1x1 grid with base."""
        grid = GridPattern()
        mesh = grid.generate(width=1, depth=1, include_base=True)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_1x1_without_base(self):
        """Test generating 1x1 grid without base."""
        grid = GridPattern()
        mesh = grid.generate(width=1, depth=1, include_base=False)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_2x2_grid(self):
        """Test generating 2x2 grid."""
        grid = GridPattern()
        mesh = grid.generate(width=2, depth=2, include_base=True)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_3x3_grid(self):
        """Test generating 3x3 grid."""
        grid = GridPattern()
        mesh = grid.generate(width=3, depth=3, include_base=True)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_asymmetric_grid(self):
        """Test generating asymmetric grid."""
        grid = GridPattern()
        mesh = grid.generate(width=2, depth=5, include_base=True)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_large_grid(self):
        """Test generating larger grid."""
        grid = GridPattern()
        mesh = grid.generate(width=10, depth=10, include_base=True)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_grid_lays_on_xy_plane(self):
        """Test that generated grid has basis at origin (0,0,0)."""
        grid = GridPattern()
        mesh = grid.generate(width=3, depth=3, include_base=True)
        
        # Get all vertices
        all_vertices = mesh.vectors.reshape(-1, 3)
        
        # Verify minimum coordinates are at origin
        min_x = all_vertices[:, 0].min()
        min_y = all_vertices[:, 1].min()
        min_z = all_vertices[:, 2].min()
        
        assert min_x == 0.0, f"Grid should start at X=0, but min X is {min_x}"
        assert min_y == 0.0, f"Grid should start at Y=0, but min Y is {min_y}"
        assert min_z == 0.0, f"Grid should start at Z=0, but min Z is {min_z}"
