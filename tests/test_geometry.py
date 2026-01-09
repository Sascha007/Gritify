"""Unit tests for geometry module."""

import pytest
import numpy as np
from gritify.geometry import GridfinityBase


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
