"""Grid pattern generator module for Gridfinity."""

from gritify.geometry import GridfinityBase


class GridPattern(GridfinityBase):
    """Generator for Gridfinity grid patterns."""
    
    def generate(self, width, depth, include_base=True):
        """
        Generate a grid pattern.
        
        Args:
            width: Number of grid units in width
            depth: Number of grid units in depth
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
        
        # Vertical dividers
        for i in range(width + 1):
            x = i * self.base_size
            divider = self.create_box(
                center=(x, plate_depth / 2, divider_height / 2),
                size=(divider_thickness, plate_depth, divider_height)
            )
            meshes.append(divider)
        
        # Horizontal dividers
        for j in range(depth + 1):
            y = j * self.base_size
            divider = self.create_box(
                center=(plate_width / 2, y, divider_height / 2),
                size=(plate_width, divider_thickness, divider_height)
            )
            meshes.append(divider)
        
        return self.combine_meshes(meshes)
