"""Unit tests for geometry module."""

import pytest
import numpy as np
import math
from gritify.geometry import (
    GridfinityBase,
    create_rounded_rectangle_path,
    create_baseplate_cell_outline,
    create_bin_footprint_outline
)


class TestGridfinityBase:
    """Test cases for GridfinityBase class."""
    
    def test_init_default_values(self):
        """Test initialization with default values."""
        base = GridfinityBase()
        assert base.base_size == 42.0
        assert base.height_unit == 7.0
        assert base.tolerance == 0.5
    
    def test_init_custom_values(self):
        """Test initialization with custom values."""
        base = GridfinityBase(base_size=50.0, height_unit=10.0, tolerance=1.0)
        assert base.base_size == 50.0
        assert base.height_unit == 10.0
        assert base.tolerance == 1.0
    
    def test_create_box_basic(self):
        """Test basic box creation."""
        base = GridfinityBase()
        mesh = base.create_box(center=(0, 0, 0), size=(10, 10, 10))
        
        # Mesh should have 12 faces (2 per side, 6 sides)
        assert mesh.data.size == 12
        assert mesh.vectors.shape == (12, 3, 3)
    
    def test_create_box_dimensions(self):
        """Test box with specific dimensions."""
        base = GridfinityBase()
        center = (5, 5, 5)
        size = (20, 30, 40)
        mesh = base.create_box(center=center, size=size)
        
        # Check that vertices are within expected bounds
        all_vertices = mesh.vectors.reshape(-1, 3)
        
        # X bounds: center_x ± width/2 = 5 ± 10 = [-5, 15]
        assert np.min(all_vertices[:, 0]) >= -5.1
        assert np.max(all_vertices[:, 0]) <= 15.1
        
        # Y bounds: center_y ± depth/2 = 5 ± 15 = [-10, 20]
        assert np.min(all_vertices[:, 1]) >= -10.1
        assert np.max(all_vertices[:, 1]) <= 20.1
        
        # Z bounds: center_z ± height/2 = 5 ± 20 = [-15, 25]
        assert np.min(all_vertices[:, 2]) >= -15.1
        assert np.max(all_vertices[:, 2]) <= 25.1
    
    def test_combine_meshes_empty(self):
        """Test combining empty list of meshes."""
        base = GridfinityBase()
        result = base.combine_meshes([])
        assert result is None
    
    def test_combine_meshes_single(self):
        """Test combining single mesh."""
        base = GridfinityBase()
        mesh1 = base.create_box((0, 0, 0), (10, 10, 10))
        result = base.combine_meshes([mesh1])
        
        assert result is mesh1
        assert result.data.size == 12
    
    def test_combine_meshes_multiple(self):
        """Test combining multiple meshes."""
        base = GridfinityBase()
        mesh1 = base.create_box((0, 0, 0), (10, 10, 10))
        mesh2 = base.create_box((20, 0, 0), (10, 10, 10))
        mesh3 = base.create_box((40, 0, 0), (10, 10, 10))
        
        result = base.combine_meshes([mesh1, mesh2, mesh3])
        
        # Total faces should be sum of all meshes
        assert result.data.size == 36  # 12 + 12 + 12


class TestRoundedRectanglePath:
    """Test cases for rounded rectangle path generation."""
    
    def test_basic_rounded_rectangle(self):
        """Test basic rounded rectangle path creation."""
        path = create_rounded_rectangle_path(x=0, y=0, w=10, h=10, r=2)
        
        # Path should be non-empty
        assert len(path) > 0
        
        # Path should be closed (first and last points are the same)
        assert path[0] == path[-1]
    
    def test_radius_clamping(self):
        """Test that radius is clamped to half the minimum dimension."""
        # Try to create a rectangle with radius larger than possible
        path = create_rounded_rectangle_path(x=0, y=0, w=10, h=10, r=10)
        
        # Should still create a valid path (radius clamped to 5)
        assert len(path) > 0
        assert path[0] == path[-1]
    
    def test_zero_radius(self):
        """Test rectangle with zero radius (sharp corners)."""
        path = create_rounded_rectangle_path(x=0, y=0, w=10, h=10, r=0, segments_per_arc=1)
        
        # Should still create a closed path
        assert len(path) > 0
        assert path[0] == path[-1]
    
    def test_path_bounds(self):
        """Test that path stays within expected bounds."""
        x, y, w, h, r = 5, 10, 20, 30, 3
        path = create_rounded_rectangle_path(x=x, y=y, w=w, h=h, r=r)
        
        # Extract all x and y coordinates
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        
        # Check bounds (with small tolerance for floating point)
        assert min(x_coords) >= x - 0.01
        assert max(x_coords) <= x + w + 0.01
        assert min(y_coords) >= y - 0.01
        assert max(y_coords) <= y + h + 0.01
    
    def test_gridfinity_dimensions(self):
        """Test with actual Gridfinity dimensions."""
        # Single baseplate cell: 42x42mm with 8mm radius
        path = create_rounded_rectangle_path(x=0, y=0, w=42, h=42, r=8)
        
        assert len(path) > 0
        assert path[0] == path[-1]
        
        # Bin footprint: 41.5x41.5mm with 3.75mm radius
        path = create_rounded_rectangle_path(x=0.25, y=0.25, w=41.5, h=41.5, r=3.75)
        
        assert len(path) > 0
        assert path[0] == path[-1]


class TestBaseplateOutline:
    """Test cases for baseplate cell outline generation."""
    
    def test_single_cell_at_origin(self):
        """Test baseplate cell at origin (0, 0)."""
        path = create_baseplate_cell_outline(i=0, j=0)
        
        # Should create a closed path
        assert len(path) > 0
        assert path[0] == path[-1]
        
        # Check approximate bounds (42x42 starting at origin)
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        
        assert min(x_coords) >= -0.01
        assert max(x_coords) <= 42.01
        assert min(y_coords) >= -0.01
        assert max(y_coords) <= 42.01
    
    def test_offset_cell(self):
        """Test baseplate cell at offset position."""
        path = create_baseplate_cell_outline(i=2, j=3, grid_pitch=42.0)
        
        # Should be offset by (2*42, 3*42) = (84, 126)
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        
        assert min(x_coords) >= 84 - 0.01
        assert max(x_coords) <= 126.01
        assert min(y_coords) >= 126 - 0.01
        assert max(y_coords) <= 168.01
    
    def test_custom_grid_pitch(self):
        """Test with custom grid pitch."""
        path = create_baseplate_cell_outline(i=0, j=0, grid_pitch=50.0)
        
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        
        # Should be 50x50
        assert max(x_coords) <= 50.01
        assert max(y_coords) <= 50.01


class TestBinFootprintOutline:
    """Test cases for bin/block footprint outline generation."""
    
    def test_single_cell_bin(self):
        """Test 1x1 bin footprint."""
        path = create_bin_footprint_outline(i=0, j=0, nx=1, ny=1)
        
        # Should create a closed path
        assert len(path) > 0
        assert path[0] == path[-1]
        
        # Size should be 41.5x41.5 (42 - 2*0.25)
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        
        # Min should be around 0.25 (clearance)
        assert min(x_coords) >= 0.24
        assert min(y_coords) >= 0.24
        
        # Max should be around 41.75 (0.25 + 41.5)
        assert max(x_coords) <= 41.76
        assert max(y_coords) <= 41.76
    
    def test_multi_cell_bin(self):
        """Test 2x3 bin footprint."""
        path = create_bin_footprint_outline(i=0, j=0, nx=2, ny=3)
        
        assert len(path) > 0
        assert path[0] == path[-1]
        
        # Width: 2*42 - 2*0.25 = 84 - 0.5 = 83.5
        # Height: 3*42 - 2*0.25 = 126 - 0.5 = 125.5
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        
        assert min(x_coords) >= 0.24
        assert max(x_coords) <= 83.76  # 0.25 + 83.5
        assert min(y_coords) >= 0.24
        assert max(y_coords) <= 125.76  # 0.25 + 125.5
    
    def test_offset_bin(self):
        """Test bin at offset grid position."""
        path = create_bin_footprint_outline(i=1, j=1, nx=1, ny=1)
        
        # Should be offset by (1*42, 1*42) = (42, 42)
        # Plus clearance of 0.25
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        
        assert min(x_coords) >= 42.24
        assert min(y_coords) >= 42.24
    
    def test_custom_clearance(self):
        """Test with custom clearance value."""
        path = create_bin_footprint_outline(
            i=0, j=0, nx=1, ny=1,
            xy_clearance_per_side=0.5
        )
        
        # With 0.5mm clearance per side, size should be 42 - 2*0.5 = 41
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        
        assert min(x_coords) >= 0.49
        assert max(x_coords) <= 41.51  # 0.5 + 41
