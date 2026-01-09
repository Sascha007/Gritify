"""Grid pattern generator module for Gridfinity.

Generates grid patterns with their base positioned at the origin (0, 0, 0),
ready for 3D printing on the XY plane.
"""

import numpy as np
from gritify.geometry import GridfinityBase


class GridPattern(GridfinityBase):
    """Generator for Gridfinity grid patterns."""
    
    def generate(self, width, depth, include_base=True):
        """
        Generate a grid pattern.
        Supports half grids (0.5 unit increments) for better space utilization.
        
        Args:
            width: Number of grid units in width (supports 0.5 increments)
            depth: Number of grid units in depth (supports 0.5 increments)
            include_base: Whether to include base plate (default True)
            
        Returns:
            numpy-stl mesh object
        """
        meshes = []
        
        # Base plate dimensions
        base_height = 5.0 if include_base else 0
        plate_width = width * self.base_size
        plate_depth = depth * self.base_size
        
        if include_base:
            # Create base plate
            base_plate = self.create_box(
                center=(plate_width / 2, plate_depth / 2, base_height / 2),
                size=(plate_width, plate_depth, base_height)
            )
            meshes.append(base_plate)
        
        # Add grid dividers (simplified version)
        divider_thickness = 1.0
        divider_height = base_height + 2.0
        
        # Calculate number of dividers for half grids
        # Use ceil to ensure we have dividers at fractional positions
        num_dividers_x = int(np.ceil(width)) + 1
        num_dividers_y = int(np.ceil(depth)) + 1
        
        # Vertical dividers
        for i in range(num_dividers_x):
            x = min(i * self.base_size, plate_width)
            divider = self.create_box(
                center=(x, plate_depth / 2, divider_height / 2),
                size=(divider_thickness, plate_depth, divider_height)
            )
            meshes.append(divider)
        
        # Horizontal dividers
        for j in range(num_dividers_y):
            y = min(j * self.base_size, plate_depth)
            divider = self.create_box(
                center=(plate_width / 2, y, divider_height / 2),
                size=(plate_width, divider_thickness, divider_height)
            )
            meshes.append(divider)
        
        return self.combine_meshes(meshes)
