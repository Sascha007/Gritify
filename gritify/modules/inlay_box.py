"""Inlay box generator module for Gridfinity.

Generates inlay boxes with internal divisions, positioned at the origin (0, 0, 0),
ready for 3D printing on the XY plane.
"""

from gritify.geometry import GridfinityBase


class InlayBox(GridfinityBase):
    """Generator for Gridfinity inlay boxes with compartments."""
    
    def generate(self, width, depth, height, divisions_x=2, divisions_y=2, wall_thickness=1.5):
        """
        Generate a Gridfinity inlay box with internal divisions.
        
        Args:
            width: Number of grid units in width
            depth: Number of grid units in depth
            height: Number of height units
            divisions_x: Number of divisions in X direction (default 2)
            divisions_y: Number of divisions in Y direction (default 2)
            wall_thickness: Thickness of walls in mm (default 1.5)
            
        Returns:
            numpy-stl mesh object
        """
        meshes = []
        
        # Calculate dimensions
        outer_width = width * self.base_size - self.tolerance
        outer_depth = depth * self.base_size - self.tolerance
        total_height = height * self.height_unit
        
        # Base height
        base_height = 5.0
        
        # Create base
        base = self.create_box(
            center=(outer_width / 2, outer_depth / 2, base_height / 2),
            size=(outer_width, outer_depth, base_height)
        )
        meshes.append(base)
        
        # Wall height
        wall_height = total_height - base_height
        
        # Create outer walls
        # Front and back walls
        for y_pos in [wall_thickness / 2, outer_depth - wall_thickness / 2]:
            wall = self.create_box(
                center=(outer_width / 2, y_pos, base_height + wall_height / 2),
                size=(outer_width, wall_thickness, wall_height)
            )
            meshes.append(wall)
        
        # Left and right walls
        for x_pos in [wall_thickness / 2, outer_width - wall_thickness / 2]:
            wall = self.create_box(
                center=(x_pos, outer_depth / 2, base_height + wall_height / 2),
                size=(wall_thickness, outer_depth - 2 * wall_thickness, wall_height)
            )
            meshes.append(wall)
        
        # Create internal divisions
        usable_width = outer_width - 2 * wall_thickness
        usable_depth = outer_depth - 2 * wall_thickness
        
        # Vertical dividers (along X axis)
        if divisions_x > 1:
            for i in range(1, divisions_x):
                x_pos = wall_thickness + (i * usable_width / divisions_x)
                divider = self.create_box(
                    center=(x_pos, outer_depth / 2, base_height + wall_height / 2),
                    size=(wall_thickness, usable_depth, wall_height)
                )
                meshes.append(divider)
        
        # Horizontal dividers (along Y axis)
        if divisions_y > 1:
            for j in range(1, divisions_y):
                y_pos = wall_thickness + (j * usable_depth / divisions_y)
                divider = self.create_box(
                    center=(outer_width / 2, y_pos, base_height + wall_height / 2),
                    size=(usable_width, wall_thickness, wall_height)
                )
                meshes.append(divider)
        
        return self.combine_meshes(meshes)
