"""Unit tests for box module."""

import pytest
import numpy as np
from gritify.modules.box import Box


class TestBox:
    """Test cases for Box class."""
    
    def test_init(self):
        """Test Box initialization."""
        box = Box()
        assert box.base_size == 42.0
        assert box.height_unit == 7.0
        assert box.tolerance == 0.5
    
    def test_generate_1x1x1_box(self):
        """Test generating 1x1x1 box."""
        box = Box()
        mesh = box.generate(width=1, depth=1, height=1)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_with_default_wall_thickness(self):
        """Test generating box with default wall thickness."""
        box = Box()
        mesh = box.generate(width=2, depth=2, height=2)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_with_custom_wall_thickness(self):
        """Test generating box with custom wall thickness."""
        box = Box()
        mesh = box.generate(width=2, depth=2, height=2, wall_thickness=3.0)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_tall_box(self):
        """Test generating tall box."""
        box = Box()
        mesh = box.generate(width=1, depth=1, height=5)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_wide_box(self):
        """Test generating wide box."""
        box = Box()
        mesh = box.generate(width=5, depth=3, height=2)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_thin_walls(self):
        """Test generating box with thin walls."""
        box = Box()
        mesh = box.generate(width=2, depth=2, height=2, wall_thickness=1.0)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_thick_walls(self):
        """Test generating box with thick walls."""
        box = Box()
        mesh = box.generate(width=3, depth=3, height=3, wall_thickness=5.0)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_box_lays_on_xy_plane(self):
        """Test that generated box has basis at origin (0,0,0)."""
        box = Box()
        mesh = box.generate(width=2, depth=2, height=2)
        
        # Get all vertices
        all_vertices = mesh.vectors.reshape(-1, 3)
        
        # Verify minimum coordinates are at origin
        min_x = all_vertices[:, 0].min()
        min_y = all_vertices[:, 1].min()
        min_z = all_vertices[:, 2].min()
        
        assert min_x == 0.0, f"Box should start at X=0, but min X is {min_x}"
        assert min_y == 0.0, f"Box should start at Y=0, but min Y is {min_y}"
        assert min_z == 0.0, f"Box should start at Z=0, but min Z is {min_z}"
