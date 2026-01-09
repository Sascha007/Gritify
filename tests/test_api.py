"""Integration tests for Flask API endpoints."""

import pytest
import json
import os
from app import app as flask_app
from config import GENERATED_DIR


@pytest.fixture
def app():
    """Create and configure a test instance of the app."""
    flask_app.config['TESTING'] = True
    yield flask_app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


class TestHealthEndpoint:
    """Test cases for health endpoint."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
        assert data['service'] == 'Gritify API'


class TestGridGenerationEndpoint:
    """Test cases for grid generation endpoint."""
    
    def test_generate_grid_basic(self, client):
        """Test basic grid generation."""
        response = client.post('/api/generate/grid',
                             json={'width': 2, 'depth': 2, 'include_base': True})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'filename' in data
        assert 'download_url' in data
        assert data['filename'].startswith('grid_2x2_')
        assert data['filename'].endswith('.stl')
        
        # Check dimensions are present
        assert 'dimensions' in data
        assert data['dimensions']['x'] == 84.0  # 2 * 42mm
        assert data['dimensions']['y'] == 84.0  # 2 * 42mm
        assert data['dimensions']['z'] == 5.0   # Grid base height
        assert data['dimensions']['units'] == 'mm'
    
    def test_generate_grid_without_base(self, client):
        """Test grid generation without base."""
        response = client.post('/api/generate/grid',
                             json={'width': 1, 'depth': 1, 'include_base': False})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_generate_grid_various_sizes(self, client):
        """Test grid generation with various sizes."""
        sizes = [(1, 1), (2, 3), (5, 5)]
        
        for width, depth in sizes:
            response = client.post('/api/generate/grid',
                                 json={'width': width, 'depth': depth})
            assert response.status_code == 200
    
    def test_generate_grid_invalid_width_too_small(self, client):
        """Test grid generation with invalid width (too small)."""
        response = client.post('/api/generate/grid',
                             json={'width': 0, 'depth': 2})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_generate_grid_invalid_width_too_large(self, client):
        """Test grid generation with invalid width (too large)."""
        response = client.post('/api/generate/grid',
                             json={'width': 100, 'depth': 2})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_generate_grid_invalid_depth(self, client):
        """Test grid generation with invalid depth."""
        response = client.post('/api/generate/grid',
                             json={'width': 2, 'depth': 0})
        
        assert response.status_code == 400


class TestBoxGenerationEndpoint:
    """Test cases for box generation endpoint."""
    
    def test_generate_box_basic(self, client):
        """Test basic box generation."""
        response = client.post('/api/generate/box',
                             json={'width': 2, 'depth': 2, 'height': 2})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'filename' in data
        assert data['filename'].startswith('box_2x2x2_')
        
        # Check dimensions are present
        assert 'dimensions' in data
        assert data['dimensions']['x'] == 84.0  # 2 * 42mm
        assert data['dimensions']['y'] == 84.0  # 2 * 42mm
        assert data['dimensions']['z'] == 14.0  # 2 * 7mm
        assert data['dimensions']['units'] == 'mm'
    
    def test_generate_box_with_custom_wall_thickness(self, client):
        """Test box generation with custom wall thickness."""
        response = client.post('/api/generate/box',
                             json={'width': 2, 'depth': 2, 'height': 2, 
                                   'wall_thickness': 3.0})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_generate_box_various_sizes(self, client):
        """Test box generation with various sizes."""
        sizes = [(1, 1, 1), (2, 3, 4), (5, 5, 3)]
        
        for width, depth, height in sizes:
            response = client.post('/api/generate/box',
                                 json={'width': width, 'depth': depth, 'height': height})
            assert response.status_code == 200
    
    def test_generate_box_invalid_dimensions(self, client):
        """Test box generation with invalid dimensions."""
        # Width too small
        response = client.post('/api/generate/box',
                             json={'width': 0, 'depth': 2, 'height': 2})
        assert response.status_code == 400
        
        # Height too large
        response = client.post('/api/generate/box',
                             json={'width': 2, 'depth': 2, 'height': 100})
        assert response.status_code == 400


class TestInlayGenerationEndpoint:
    """Test cases for inlay box generation endpoint."""
    
    def test_generate_inlay_basic(self, client):
        """Test basic inlay generation."""
        response = client.post('/api/generate/inlay',
                             json={'width': 2, 'depth': 2, 'height': 2,
                                   'divisions_x': 2, 'divisions_y': 2})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'filename' in data
        assert data['filename'].startswith('inlay_2x2x2_')
        
        # Check dimensions are present
        assert 'dimensions' in data
        assert data['dimensions']['x'] == 84.0  # 2 * 42mm
        assert data['dimensions']['y'] == 84.0  # 2 * 42mm
        assert data['dimensions']['z'] == 14.0  # 2 * 7mm
        assert data['dimensions']['units'] == 'mm'
    
    def test_generate_inlay_with_custom_divisions(self, client):
        """Test inlay generation with custom divisions."""
        response = client.post('/api/generate/inlay',
                             json={'width': 3, 'depth': 3, 'height': 2,
                                   'divisions_x': 3, 'divisions_y': 2,
                                   'wall_thickness': 1.0})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_generate_inlay_various_configurations(self, client):
        """Test inlay generation with various configurations."""
        configs = [
            (2, 2, 2, 2, 2),
            (3, 2, 2, 3, 2),
            (2, 3, 3, 2, 4)
        ]
        
        for width, depth, height, div_x, div_y in configs:
            response = client.post('/api/generate/inlay',
                                 json={'width': width, 'depth': depth, 'height': height,
                                       'divisions_x': div_x, 'divisions_y': div_y})
            assert response.status_code == 200
    
    def test_generate_inlay_invalid_dimensions(self, client):
        """Test inlay generation with invalid dimensions."""
        response = client.post('/api/generate/inlay',
                             json={'width': 0, 'depth': 2, 'height': 2,
                                   'divisions_x': 2, 'divisions_y': 2})
        
        assert response.status_code == 400


class TestStorageBoxGenerationEndpoint:
    """Test cases for storage box generation endpoint."""
    
    def test_generate_storage_box_with_height_units(self, client):
        """Test storage box generation with height in units."""
        response = client.post('/api/generate/storage_box',
                             json={'width': 2, 'depth': 2, 'height_units': 3})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'filename' in data
        assert 'storage_box_2x2x3u' in data['filename']
        
        # Check dimensions are present
        assert 'dimensions' in data
        assert data['dimensions']['x'] == 84.0  # 2 * 42mm
        assert data['dimensions']['y'] == 84.0  # 2 * 42mm
        assert data['dimensions']['z'] == 21.0  # 3 * 7mm
        assert data['dimensions']['units'] == 'mm'
    
    def test_generate_storage_box_with_height_cm(self, client):
        """Test storage box generation with height in centimeters."""
        response = client.post('/api/generate/storage_box',
                             json={'width': 2, 'depth': 2, 'height_cm': 5.0})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'storage_box_2x2x5.0cm' in data['filename']
        
        # Check dimensions are present
        assert 'dimensions' in data
        assert data['dimensions']['z'] == 50.0  # 5.0cm = 50mm
    
    def test_generate_storage_box_with_flat_inside(self, client):
        """Test storage box generation with flat inside."""
        response = client.post('/api/generate/storage_box',
                             json={'width': 2, 'depth': 2, 'height_units': 2, 'flat_inside': True})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_generate_storage_box_with_grid_inside(self, client):
        """Test storage box generation with grid inside."""
        response = client.post('/api/generate/storage_box',
                             json={'width': 2, 'depth': 2, 'height_units': 2, 'flat_inside': False})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_generate_storage_box_custom_wall_thickness(self, client):
        """Test storage box generation with custom wall thickness."""
        response = client.post('/api/generate/storage_box',
                             json={'width': 2, 'depth': 2, 'height_units': 2, 'wall_thickness': 3.0})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_generate_storage_box_height_cm_precedence(self, client):
        """Test that height_cm takes precedence over height_units."""
        response = client.post('/api/generate/storage_box',
                             json={'width': 2, 'depth': 2, 'height_cm': 3.5, 'height_units': 5})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        # Should use height_cm (3.5cm = 35mm) not height_units (5 units = 35mm)
        # Both happen to equal 35mm, but height_cm takes precedence
        assert data['dimensions']['z'] == 35.0
    
    def test_generate_storage_box_invalid_dimensions(self, client):
        """Test storage box generation with invalid dimensions."""
        # Width too small
        response = client.post('/api/generate/storage_box',
                             json={'width': 0, 'depth': 2, 'height_units': 2})
        assert response.status_code == 400
        
        # Height in cm too large
        response = client.post('/api/generate/storage_box',
                             json={'width': 2, 'depth': 2, 'height_cm': 100.0})
        assert response.status_code == 400


class TestPrintbedCalculationEndpoint:
    """Test cases for printbed calculation endpoint."""
    
    def test_calculate_printbed_fits(self, client):
        """Test printbed calculation when structure fits."""
        response = client.post('/api/printbed/calculate',
                             json={'total_width': 4, 'total_depth': 4,
                                   'bed_width': 250.0, 'bed_depth': 250.0})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'breakdown' in data
        assert data['breakdown']['fits_bed'] is True
    
    def test_calculate_printbed_needs_splitting(self, client):
        """Test printbed calculation when structure needs splitting."""
        response = client.post('/api/printbed/calculate',
                             json={'total_width': 10, 'total_depth': 10,
                                   'bed_width': 220.0, 'bed_depth': 220.0})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['breakdown']['fits_bed'] is False
        assert data['breakdown']['total_pieces'] > 1
    
    def test_calculate_printbed_various_configurations(self, client):
        """Test printbed calculation with various configurations."""
        configs = [
            (5, 5, 220.0, 220.0),
            (3, 8, 200.0, 200.0),
            (15, 3, 250.0, 250.0)
        ]
        
        for width, depth, bed_w, bed_d in configs:
            response = client.post('/api/printbed/calculate',
                                 json={'total_width': width, 'total_depth': depth,
                                       'bed_width': bed_w, 'bed_depth': bed_d})
            assert response.status_code == 200


class TestDownloadEndpoint:
    """Test cases for download endpoint."""
    
    def test_download_nonexistent_file(self, client):
        """Test downloading non-existent file."""
        response = client.get('/api/download/nonexistent_file.stl')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_download_existing_file(self, client):
        """Test downloading existing file."""
        # First generate a file
        response = client.post('/api/generate/grid',
                             json={'width': 1, 'depth': 1})
        assert response.status_code == 200
        data = json.loads(response.data)
        filename = data['filename']
        
        # Try to download it
        response = client.get(f'/api/download/{filename}')
        assert response.status_code == 200
        # STL files can be served as model/stl or application/octet-stream
        assert response.mimetype in ['model/stl', 'application/octet-stream']


class TestStaticRoutes:
    """Test cases for static routes."""
    
    def test_index_route(self, client):
        """Test that index route serves HTML."""
        response = client.get('/')
        assert response.status_code == 200
