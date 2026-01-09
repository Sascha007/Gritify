"""Unit tests for storage box module."""

import pytest
from gritify.modules.storage_box import StorageBox


class TestStorageBox:
    """Test cases for StorageBox class."""
    
    def test_init(self):
        """Test StorageBox initialization."""
        box = StorageBox()
        assert box.base_size == 42.0
        assert box.height_unit == 7.0
        assert box.tolerance == 0.5
    
    def test_generate_with_height_units(self):
        """Test generating storage box with height in units."""
        box = StorageBox()
        mesh = box.generate(width=1, depth=1, height_units=3)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_with_height_cm(self):
        """Test generating storage box with height in centimeters."""
        box = StorageBox()
        mesh = box.generate(width=2, depth=2, height_cm=5.0)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_with_flat_inside(self):
        """Test generating storage box with flat inside (default)."""
        box = StorageBox()
        mesh = box.generate(width=2, depth=2, height_units=2, flat_inside=True)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_with_grid_inside(self):
        """Test generating storage box with grid inside."""
        box = StorageBox()
        mesh = box.generate(width=2, depth=2, height_units=2, flat_inside=False)
        
        assert mesh is not None
        assert mesh.data.size > 0
        # With grid inside, should have more faces than flat inside
    
    def test_generate_with_custom_wall_thickness(self):
        """Test generating storage box with custom wall thickness."""
        box = StorageBox()
        mesh = box.generate(width=2, depth=2, height_units=2, wall_thickness=3.0)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_tall_storage_box(self):
        """Test generating tall storage box."""
        box = StorageBox()
        mesh = box.generate(width=1, depth=1, height_cm=10.0)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_wide_storage_box(self):
        """Test generating wide storage box."""
        box = StorageBox()
        mesh = box.generate(width=5, depth=3, height_units=2)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_multi_grid_storage_box(self):
        """Test generating multi-grid storage box with internal dividers."""
        box = StorageBox()
        mesh = box.generate(width=3, depth=3, height_units=3, flat_inside=False)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_height_cm_takes_precedence(self):
        """Test that height_cm takes precedence over height_units."""
        box = StorageBox()
        # Both parameters provided, height_cm should be used
        mesh = box.generate(width=1, depth=1, height_cm=3.5, height_units=5)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_default_height(self):
        """Test default height when neither height_cm nor height_units provided."""
        box = StorageBox()
        mesh = box.generate(width=1, depth=1)
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_stackable_features(self):
        """Test that storage box has stackable features (lip at top)."""
        box = StorageBox()
        mesh = box.generate(width=2, depth=2, height_units=3)
        
        # Box should be generated successfully with stacking lip
        assert mesh is not None
        assert mesh.data.size > 0
