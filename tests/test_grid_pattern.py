"""Unit tests for grid_pattern module."""

import pytest
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
    
    def test_generate_half_grid_width(self):
        """Test generating grid with half unit width."""
        grid = GridPattern()
        mesh = grid.generate(width=1.5, depth=1, include_base=True)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_half_grid_depth(self):
        """Test generating grid with half unit depth."""
        grid = GridPattern()
        mesh = grid.generate(width=1, depth=2.5, include_base=True)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_half_grid_both_dimensions(self):
        """Test generating grid with half units in both dimensions."""
        grid = GridPattern()
        mesh = grid.generate(width=2.5, depth=3.5, include_base=True)
        
        assert mesh is not None
        assert mesh.data.size > 0
