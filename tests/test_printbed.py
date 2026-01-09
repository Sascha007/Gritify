"""Unit tests for printbed module."""

import pytest
from gritify.modules.printbed import PrintbedBreakdown


class TestPrintbedBreakdown:
    """Test cases for PrintbedBreakdown class."""
    
    def test_init(self):
        """Test PrintbedBreakdown initialization."""
        breakdown = PrintbedBreakdown()
        assert breakdown.base_size == 42.0
        assert breakdown.height_unit == 7.0
        assert breakdown.tolerance == 0.5
    
    def test_calculate_breakdown_fits_bed(self):
        """Test breakdown calculation when structure fits bed."""
        breakdown = PrintbedBreakdown()
        result = breakdown.calculate_breakdown(
            total_width=4, 
            total_depth=4, 
            bed_length_x=250.0, 
            bed_length_y=250.0
        )
        
        assert result['fits_bed'] is True
        assert result['pieces_x'] == 1
        assert result['pieces_y'] == 1
        assert result['total_pieces'] == 1
        assert len(result['pieces']) == 1
    
    def test_calculate_breakdown_needs_splitting(self):
        """Test breakdown calculation when structure needs splitting."""
        breakdown = PrintbedBreakdown()
        result = breakdown.calculate_breakdown(
            total_width=10,
            total_depth=10,
            bed_length_x=220.0,
            bed_length_y=220.0
        )
        
        assert result['fits_bed'] is False
        assert result['pieces_x'] >= 2
        assert result['pieces_y'] >= 2
        assert result['total_pieces'] > 1
        assert len(result['pieces']) == result['total_pieces']
    
    def test_calculate_breakdown_wide_structure(self):
        """Test breakdown for wide structure."""
        breakdown = PrintbedBreakdown()
        result = breakdown.calculate_breakdown(
            total_width=15,
            total_depth=3,
            bed_length_x=220.0,
            bed_length_y=220.0
        )
        
        assert result['pieces_x'] >= 2
        assert result['total_pieces'] >= 2
    
    def test_calculate_breakdown_deep_structure(self):
        """Test breakdown for deep structure."""
        breakdown = PrintbedBreakdown()
        result = breakdown.calculate_breakdown(
            total_width=3,
            total_depth=15,
            bed_length_x=220.0,
            bed_length_y=220.0
        )
        
        assert result['pieces_y'] >= 2
        assert result['total_pieces'] >= 2
    
    def test_calculate_breakdown_small_bed(self):
        """Test breakdown for very small printer bed."""
        breakdown = PrintbedBreakdown()
        result = breakdown.calculate_breakdown(
            total_width=5,
            total_depth=5,
            bed_length_x=100.0,
            bed_length_y=100.0
        )
        
        assert result['total_pieces'] > 1
        assert len(result['pieces']) == result['total_pieces']
    
    def test_calculate_breakdown_large_bed(self):
        """Test breakdown for large printer bed."""
        breakdown = PrintbedBreakdown()
        result = breakdown.calculate_breakdown(
            total_width=5,
            total_depth=5,
            bed_length_x=400.0,
            bed_length_y=400.0
        )
        
        assert result['fits_bed'] is True
        assert result['total_pieces'] == 1
    
    def test_calculate_breakdown_piece_dimensions(self):
        """Test that piece dimensions are calculated correctly."""
        breakdown = PrintbedBreakdown()
        result = breakdown.calculate_breakdown(
            total_width=6,
            total_depth=6,
            bed_length_x=220.0,
            bed_length_y=220.0
        )
        
        # Verify piece dimensions are reasonable
        assert result['piece_width'] > 0
        assert result['piece_depth'] > 0
        assert result['piece_width_mm'] > 0
        assert result['piece_depth_mm'] > 0
    
    def test_generate_piece_basic(self):
        """Test generating a piece from breakdown."""
        breakdown = PrintbedBreakdown()
        mesh = breakdown.generate_piece(
            total_width=4,
            total_depth=4,
            height=2,
            piece_x=0,
            piece_y=0,
            pieces_x=2,
            pieces_y=2
        )
        
        assert mesh is not None
        assert mesh.data.size > 0
    
    def test_generate_piece_different_indices(self):
        """Test generating different pieces."""
        breakdown = PrintbedBreakdown()
        
        # Generate multiple pieces
        mesh1 = breakdown.generate_piece(4, 4, 2, 0, 0, 2, 2)
        mesh2 = breakdown.generate_piece(4, 4, 2, 1, 0, 2, 2)
        mesh3 = breakdown.generate_piece(4, 4, 2, 0, 1, 2, 2)
        
        assert mesh1 is not None
        assert mesh2 is not None
        assert mesh3 is not None
    
    def test_calculate_breakdown_with_half_grids(self):
        """Test breakdown calculation that uses half grids."""
        breakdown = PrintbedBreakdown()
        result = breakdown.calculate_breakdown(
            total_width=7,
            total_depth=7,
            bed_length_x=220.0,
            bed_length_y=220.0
        )
        
        # Check if half grids are being used (piece sizes should be 0.5 increments)
        assert 'uses_half_grids' in result
        # Verify piece width/depth are in 0.5 increments
        assert result['piece_width'] % 0.5 == 0
        assert result['piece_depth'] % 0.5 == 0
    
    def test_calculate_breakdown_with_spacers(self):
        """Test breakdown calculation that includes spacers."""
        breakdown = PrintbedBreakdown()
        result = breakdown.calculate_breakdown(
            total_width=11,
            total_depth=11,
            bed_length_x=220.0,
            bed_length_y=220.0
        )
        
        # Check that spacer information is included
        assert 'spacer_x' in result
        assert 'spacer_y' in result
        assert 'spacer_x_mm' in result
        assert 'spacer_y_mm' in result
        assert 'uses_spacers' in result
        
        # Spacers should be non-negative
        assert result['spacer_x'] >= 0
        assert result['spacer_y'] >= 0
    
    def test_generate_piece_with_half_grids(self):
        """Test generating a piece that uses half grids."""
        breakdown = PrintbedBreakdown()
        
        # This should create pieces with fractional dimensions
        mesh = breakdown.generate_piece(
            total_width=3,
            total_depth=3,
            height=2,
            piece_x=0,
            piece_y=0,
            pieces_x=2,
            pieces_y=2
        )
        
        assert mesh is not None
        assert mesh.data.size > 0
