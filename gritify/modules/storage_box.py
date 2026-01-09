"""Storage box generator module for Gridfinity-compatible boxes."""

from gritify.geometry import GridfinityBase


class StorageBox(GridfinityBase):
    """Generator for Gridfinity-compatible storage boxes."""
    
    def generate(self, width, depth, height_cm=None, height_units=None, 
                 wall_thickness=2.0, flat_inside=True):
        """
        Generate a Gridfinity-compatible storage box.
        
        Args:
            width: Number of grid units in width
            depth: Number of grid units in depth
            height_cm: Height in centimeters (takes precedence if provided)
            height_units: Height in Gridfinity units (7mm each, used if height_cm not provided)
            wall_thickness: Thickness of walls in mm (default 2.0)
            flat_inside: If True, flat inside bottom; if False, includes grid pattern (default True)
            
        Returns:
            numpy-stl mesh object
        """
        meshes = []
        
        # Calculate dimensions
        outer_width = width * self.base_size - self.tolerance
        outer_depth = depth * self.base_size - self.tolerance
        
        # Determine total height
        if height_cm is not None:
            total_height = height_cm * 10.0  # Convert cm to mm
        elif height_units is not None:
            total_height = height_units * self.height_unit
        else:
            total_height = self.height_unit  # Default to 1 unit
        
        # Gridfinity-compatible base parameters
        base_height = 5.0  # Standard Gridfinity base height
        magnet_hole_diameter = 6.5
        magnet_hole_depth = 2.4
        
        # Create Gridfinity-compatible base with grid pattern
        # The base should have the characteristic Gridfinity grid attachment points
        base = self.create_box(
            center=(outer_width / 2, outer_depth / 2, base_height / 2),
            size=(outer_width, outer_depth, base_height)
        )
        meshes.append(base)
        
        # Add grid dividers to base for Gridfinity compatibility
        divider_thickness = 1.0
        divider_height = base_height + 1.0  # Slightly above base
        
        # Add vertical dividers at grid boundaries
        for i in range(1, width):
            x = i * self.base_size
            divider = self.create_box(
                center=(x, outer_depth / 2, divider_height / 2),
                size=(divider_thickness, outer_depth, divider_height)
            )
            meshes.append(divider)
        
        # Add horizontal dividers at grid boundaries
        for j in range(1, depth):
            y = j * self.base_size
            divider = self.create_box(
                center=(outer_width / 2, y, divider_height / 2),
                size=(outer_width, divider_thickness, divider_height)
            )
            meshes.append(divider)
        
        # Create walls with stackable lip
        wall_height = total_height - base_height
        lip_height = 2.0  # Height of stacking lip
        
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
        
        # Add stacking lip at the top (inner rim)
        # This allows boxes to stack securely on top of each other
        lip_inset = 1.0
        lip_thickness = 1.5
        top_z = base_height + wall_height
        
        # Front and back lips
        for y_pos in [wall_thickness + lip_inset, 
                      outer_depth - wall_thickness - lip_inset]:
            lip = self.create_box(
                center=(outer_width / 2, y_pos, top_z - lip_height / 2),
                size=(outer_width - 2 * wall_thickness, lip_thickness, lip_height)
            )
            meshes.append(lip)
        
        # Left and right lips
        for x_pos in [wall_thickness + lip_inset,
                      outer_width - wall_thickness - lip_inset]:
            lip = self.create_box(
                center=(x_pos, outer_depth / 2, top_z - lip_height / 2),
                size=(lip_thickness, outer_depth - 2 * wall_thickness - 2 * lip_thickness, lip_height)
            )
            meshes.append(lip)
        
        # If not flat_inside, add internal grid structure
        if not flat_inside:
            # Add internal grid dividers for additional storage organization
            internal_divider_height = wall_height - 1.0  # Leave space at top
            internal_z = base_height + internal_divider_height / 2
            
            # Internal vertical dividers
            for i in range(1, width):
                x = i * self.base_size
                int_divider = self.create_box(
                    center=(x, outer_depth / 2, internal_z),
                    size=(divider_thickness, outer_depth - 2 * wall_thickness, internal_divider_height)
                )
                meshes.append(int_divider)
            
            # Internal horizontal dividers
            for j in range(1, depth):
                y = j * self.base_size
                int_divider = self.create_box(
                    center=(outer_width / 2, y, internal_z),
                    size=(outer_width - 2 * wall_thickness, divider_thickness, internal_divider_height)
                )
                meshes.append(int_divider)
        
        return self.combine_meshes(meshes)
