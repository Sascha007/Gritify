"""Unit tests for inlay_box module."""

import pytest
import numpy as np
from gritify.modules.inlay_box import InlayBox


class TestInlayBox:
    """Test cases for InlayBox class."""
    
    def test_init(self):
        """Test InlayBox initialization."""
        inlay = InlayBox()
        assert inlay.base_size == 42.0
        assert inlay.height_unit == 7.0
        assert inlay.tolerance == 0.5
    
    def test_generate_basic_inlay(self):
        """Test generating basic inlay box."""
        inlay = InlayBox()
        mesh = inlay.generate(width=2, depth=2, height=2)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_with_default_divisions(self):
        """Test generating inlay with default divisions."""
        inlay = InlayBox()
        mesh = inlay.generate(width=2, depth=2, height=2, divisions_x=2, divisions_y=2)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_with_custom_divisions_x(self):
        """Test generating inlay with custom X divisions."""
        inlay = InlayBox()
        mesh = inlay.generate(width=3, depth=2, height=2, divisions_x=3, divisions_y=2)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_with_custom_divisions_y(self):
        """Test generating inlay with custom Y divisions."""
        inlay = InlayBox()
        mesh = inlay.generate(width=2, depth=3, height=2, divisions_x=2, divisions_y=3)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_no_divisions(self):
        """Test generating inlay with no divisions (single compartment)."""
        inlay = InlayBox()
        mesh = inlay.generate(width=2, depth=2, height=2, divisions_x=1, divisions_y=1)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_many_divisions(self):
        """Test generating inlay with many divisions."""
        inlay = InlayBox()
        mesh = inlay.generate(width=3, depth=3, height=2, divisions_x=4, divisions_y=4)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_with_custom_wall_thickness(self):
        """Test generating inlay with custom wall thickness."""
        inlay = InlayBox()
        mesh = inlay.generate(width=2, depth=2, height=2, 
                            divisions_x=2, divisions_y=2, wall_thickness=2.0)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_tall_inlay(self):
        """Test generating tall inlay box."""
        inlay = InlayBox()
        mesh = inlay.generate(width=2, depth=2, height=5, divisions_x=2, divisions_y=2)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_inlay_box_lays_on_xy_plane(self):
        """Test that generated inlay box has basis at origin (0,0,0)."""
        inlay = InlayBox()
        mesh = inlay.generate(width=2, depth=2, height=2)
        
        # Get all vertices
        all_vertices = mesh.vectors.reshape(-1, 3)
        
        # Verify minimum coordinates are at origin
        min_x = all_vertices[:, 0].min()
        min_y = all_vertices[:, 1].min()
        min_z = all_vertices[:, 2].min()
        
        assert min_x == 0.0, f"InlayBox should start at X=0, but min X is {min_x}"
        assert min_y == 0.0, f"InlayBox should start at Y=0, but min Y is {min_y}"
        assert min_z == 0.0, f"InlayBox should start at Z=0, but min Z is {min_z}"
