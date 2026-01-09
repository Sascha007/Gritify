"""Box generator module for Gridfinity.

Generates storage boxes with their base positioned at the origin (0, 0, 0),
ready for 3D printing on the XY plane.
"""

from gritify.geometry import GridfinityBase


class Box(GridfinityBase):
    """Generator for Gridfinity boxes."""
    
    def generate(self, width, depth, height, wall_thickness=2.0):
        """
        Generate a Gridfinity box.
        
        Args:
            width: Number of grid units in width
            depth: Number of grid units in depth
            height: Number of height units
            wall_thickness: Thickness of walls in mm (default 2.0)
            
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
        
        # Create walls
        wall_height = total_height - base_height
        
        # Front and back walls
        for y_offset, y_pos in [(0, wall_thickness / 2), 
                                (outer_depth - wall_thickness, outer_depth - wall_thickness / 2)]:
            wall = self.create_box(
                center=(outer_width / 2, y_pos, base_height + wall_height / 2),
                size=(outer_width, wall_thickness, wall_height)
            )
            meshes.append(wall)
        
        # Left and right walls
        for x_offset, x_pos in [(0, wall_thickness / 2),
                                (outer_width - wall_thickness, outer_width - wall_thickness / 2)]:
            wall = self.create_box(
                center=(x_pos, outer_depth / 2, base_height + wall_height / 2),
                size=(wall_thickness, outer_depth - 2 * wall_thickness, wall_height)
            )
            meshes.append(wall)
        
        return self.combine_meshes(meshes)
