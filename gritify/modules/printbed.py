"""Printbed breakdown module for Gridfinity structures."""

import numpy as np
from gritify.geometry import GridfinityBase
from gritify.modules.grid_pattern import GridPattern


class PrintbedBreakdown(GridfinityBase):
    """Module for breaking down large structures to fit printer bed."""
    
    def calculate_breakdown(self, total_width, total_depth, bed_length_x, bed_length_y):
        """
        Calculate how to break down a structure to fit printer bed.
        Uses half grids and spacers to optimally fill the available space.
        
        Args:
            total_width: Total width in grid units
            total_depth: Total depth in grid units
            bed_length_x: Printer bed length in X dimension (mm)
            bed_length_y: Printer bed length in Y dimension (mm)
            
        Returns:
            dict with breakdown information including half grids and spacers
        """
        # Calculate size in mm
        total_width_mm = total_width * self.base_size
        total_depth_mm = total_depth * self.base_size
        
        # Add margin for printer
        margin = 10.0  # 10mm margin
        usable_bed_x = bed_length_x - 2 * margin
        usable_bed_y = bed_length_y - 2 * margin
        
        # Calculate how many pieces needed
        pieces_x = int(np.ceil(total_width_mm / usable_bed_x))
        pieces_y = int(np.ceil(total_depth_mm / usable_bed_y))
        
        # Calculate piece sizes with half grid optimization
        piece_width = total_width / pieces_x
        piece_depth = total_depth / pieces_y
        
        # Optimize piece sizes using half grids (0.5 increments)
        # Round to nearest 0.5 for better space utilization
        piece_width_optimized = float(np.round(piece_width * 2) / 2)
        piece_depth_optimized = float(np.round(piece_depth * 2) / 2)
        
        # Calculate spacers needed to fill remaining space
        spacer_x = float(max(0, piece_width - piece_width_optimized))
        spacer_y = float(max(0, piece_depth - piece_depth_optimized))
        
        breakdown = {
            'total_pieces': int(pieces_x * pieces_y),
            'pieces_x': int(pieces_x),
            'pieces_y': int(pieces_y),
            'piece_width': float(piece_width_optimized),
            'piece_depth': float(piece_depth_optimized),
            'piece_width_mm': float(piece_width_optimized * self.base_size),
            'piece_depth_mm': float(piece_depth_optimized * self.base_size),
            'spacer_x': float(spacer_x),
            'spacer_y': float(spacer_y),
            'spacer_x_mm': float(spacer_x * self.base_size),
            'spacer_y_mm': float(spacer_y * self.base_size),
            'uses_half_grids': bool((piece_width_optimized % 1 != 0) or (piece_depth_optimized % 1 != 0)),
            'uses_spacers': bool(spacer_x > 0.01 or spacer_y > 0.01),
            'fits_bed': bool(pieces_x == 1 and pieces_y == 1),
            'pieces': []
        }
        
        # Generate piece information
        for i in range(pieces_x):
            for j in range(pieces_y):
                piece = {
                    'id': f'{i}_{j}',
                    'x_index': int(i),
                    'y_index': int(j),
                    'width': float(piece_width_optimized),
                    'depth': float(piece_depth_optimized),
                    'spacer_x': float(spacer_x if i < pieces_x - 1 else 0),
                    'spacer_y': float(spacer_y if j < pieces_y - 1 else 0)
                }
                breakdown['pieces'].append(piece)
        
        return breakdown
    
    def generate_piece(self, total_width, total_depth, height, piece_x, piece_y, 
                      pieces_x, pieces_y):
        """
        Generate a specific piece of a broken-down structure.
        Supports half grids for better space utilization.
        
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
        
        # Optimize piece sizes using half grids (0.5 increments)
        piece_width_optimized = np.round(piece_width * 2) / 2
        piece_depth_optimized = np.round(piece_depth * 2) / 2
        
        # Ensure minimum size of 0.5 units
        piece_width_optimized = max(0.5, piece_width_optimized)
        piece_depth_optimized = max(0.5, piece_depth_optimized)
        
        # Generate grid pattern with half grid support
        grid = GridPattern(self.base_size, self.height_unit, self.tolerance)
        
        return grid.generate(piece_width_optimized, piece_depth_optimized, include_base=True)
