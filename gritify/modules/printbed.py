"""Printbed breakdown module for Gridfinity structures."""

import numpy as np
from gritify.geometry import GridfinityBase


class PrintbedBreakdown(GridfinityBase):
    """Module for breaking down large structures to fit printer bed."""
    
    def calculate_breakdown(self, total_width, total_depth, bed_width, bed_depth):
        """
        Calculate how to break down a structure to fit printer bed.
        
        Args:
            total_width: Total width in grid units
            total_depth: Total depth in grid units
            bed_width: Printer bed width in mm
            bed_depth: Printer bed depth in mm
            
        Returns:
            dict with breakdown information
        """
        # Calculate size in mm
        total_width_mm = total_width * self.base_size
        total_depth_mm = total_depth * self.base_size
        
        # Add margin for printer
        margin = 10.0  # 10mm margin
        usable_bed_width = bed_width - 2 * margin
        usable_bed_depth = bed_depth - 2 * margin
        
        # Calculate how many pieces needed
        pieces_x = int(np.ceil(total_width_mm / usable_bed_width))
        pieces_y = int(np.ceil(total_depth_mm / usable_bed_depth))
        
        # Calculate piece sizes
        piece_width = total_width / pieces_x
        piece_depth = total_depth / pieces_y
        
        breakdown = {
            'total_pieces': pieces_x * pieces_y,
            'pieces_x': pieces_x,
            'pieces_y': pieces_y,
            'piece_width': piece_width,
            'piece_depth': piece_depth,
            'piece_width_mm': piece_width * self.base_size,
            'piece_depth_mm': piece_depth * self.base_size,
            'fits_bed': pieces_x == 1 and pieces_y == 1,
            'pieces': []
        }
        
        # Generate piece information
        for i in range(pieces_x):
            for j in range(pieces_y):
                piece = {
                    'id': f'{i}_{j}',
                    'x_index': i,
                    'y_index': j,
                    'width': piece_width,
                    'depth': piece_depth
                }
                breakdown['pieces'].append(piece)
        
        return breakdown
    
    def generate_piece(self, total_width, total_depth, height, piece_x, piece_y, 
                      pieces_x, pieces_y):
        """
        Generate a specific piece of a broken-down structure.
        
        Args:
            total_width: Total width in grid units
            total_depth: Total depth in grid units
            height: Height in height units
            piece_x: X index of piece (0-based)
            piece_y: Y index of piece (0-based)
            pieces_x: Total number of pieces in X
            pieces_y: Total number of pieces in Y
            
        Returns:
            numpy-stl mesh object for the piece
        """
        # Calculate piece dimensions
        piece_width = total_width / pieces_x
        piece_depth = total_depth / pieces_y
        
        # For simplicity, generate a basic grid pattern piece
        from gritify.modules.grid_pattern import GridPattern
        grid = GridPattern(self.base_size, self.height_unit, self.tolerance)
        
        # Round to nearest integer for grid units
        piece_width_units = max(1, int(np.ceil(piece_width)))
        piece_depth_units = max(1, int(np.ceil(piece_depth)))
        
        return grid.generate(piece_width_units, piece_depth_units, include_base=True)
