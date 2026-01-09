"""Base geometry utilities for Gridfinity structures.

All generated models are positioned with their basis at the origin (0, 0, 0),
ensuring they are ready for 3D printing with the base laying on the XY plane.
"""

import numpy as np
from stl import mesh
import math


class GridfinityBase:
    """Base class for Gridfinity geometry generation."""
    
    def __init__(self, base_size=42.0, height_unit=7.0, tolerance=0.5):
        """
        Initialize Gridfinity base parameters.
        
        Args:
            base_size: Base grid size in mm (default 42mm)
            height_unit: Height unit in mm (default 7mm)
            tolerance: Tolerance for fit in mm (default 0.5mm)
        """
        self.base_size = base_size
        self.height_unit = height_unit
        self.tolerance = tolerance
    
    def create_box(self, center, size):
        """
        Create a simple box mesh.
        
        Args:
            center: (x, y, z) center coordinates
            size: (width, depth, height) dimensions
            
        Returns:
            numpy-stl mesh object
            
        Note:
            The box is created centered at the given coordinates.
            To ensure the box starts at origin (0, 0, 0), set center to
            (width/2, depth/2, height/2).
        """
        cx, cy, cz = center
        w, d, h = size
        
        # Define 8 vertices of the box
        vertices = np.array([
            [cx - w/2, cy - d/2, cz - h/2],  # 0
            [cx + w/2, cy - d/2, cz - h/2],  # 1
            [cx + w/2, cy + d/2, cz - h/2],  # 2
            [cx - w/2, cy + d/2, cz - h/2],  # 3
            [cx - w/2, cy - d/2, cz + h/2],  # 4
            [cx + w/2, cy - d/2, cz + h/2],  # 5
            [cx + w/2, cy + d/2, cz + h/2],  # 6
            [cx - w/2, cy + d/2, cz + h/2],  # 7
        ])
        
        # Define 12 triangles (2 per face, 6 faces)
        faces = np.array([
            # Bottom
            [0, 1, 2], [0, 2, 3],
            # Top
            [4, 6, 5], [4, 7, 6],
            # Front
            [0, 5, 1], [0, 4, 5],
            # Back
            [3, 2, 6], [3, 6, 7],
            # Left
            [0, 3, 7], [0, 7, 4],
            # Right
            [1, 5, 6], [1, 6, 2],
        ])
        
        # Create mesh
        box_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, face in enumerate(faces):
            for j in range(3):
                box_mesh.vectors[i][j] = vertices[face[j], :]
        
        return box_mesh
    
    def combine_meshes(self, meshes):
        """
        Combine multiple meshes into one.
        
        Args:
            meshes: List of numpy-stl mesh objects
            
        Returns:
            Combined mesh object
        """
        if not meshes:
            return None
        
        if len(meshes) == 1:
            return meshes[0]
        
        # Count total faces
        total_faces = sum(m.data.size for m in meshes)
        
        # Create combined mesh
        combined = mesh.Mesh(np.zeros(total_faces, dtype=mesh.Mesh.dtype))
        
        # Copy data from all meshes
        offset = 0
        for m in meshes:
            combined.data[offset:offset + m.data.size] = m.data
            offset += m.data.size
        
        return combined


def create_rounded_rectangle_path(x, y, w, h, r, segments_per_arc=16):
    """
    Create a 2D path for a rounded rectangle with closed structure.
    
    This function generates a closed path consisting of lines and arcs
    for a rounded rectangle, following Gridfinity outline specifications.
    
    Args:
        x: X coordinate of bottom-left corner
        y: Y coordinate of bottom-left corner
        w: Width of rectangle
        h: Height of rectangle
        r: Corner radius
        segments_per_arc: Number of segments to approximate each quarter-circle arc (default 16)
    
    Returns:
        List of (x, y) coordinate tuples representing the closed path
        
    Note:
        - Radius is automatically clamped to min(r, w/2, h/2)
        - Path is closed (first point equals last point)
        - Path runs clockwise from bottom-left
    """
    # Clamp radius to ensure it doesn't exceed half the width or height
    r = min(r, w / 2, h / 2)
    
    path = []
    
    # Start at bottom-left corner, after the arc
    # Bottom edge: move right along bottom
    path.append((x + r, y))
    path.append((x + w - r, y))
    
    # Bottom-right arc (from 270° to 360°, or -90° to 0°)
    cx, cy = x + w - r, y + r
    for i in range(segments_per_arc + 1):
        angle = -math.pi / 2 + (math.pi / 2) * (i / segments_per_arc)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        path.append((px, py))
    
    # Right edge: move up along right side
    path.append((x + w, y + r))
    path.append((x + w, y + h - r))
    
    # Top-right arc (from 0° to 90°)
    cx, cy = x + w - r, y + h - r
    for i in range(segments_per_arc + 1):
        angle = 0 + (math.pi / 2) * (i / segments_per_arc)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        path.append((px, py))
    
    # Top edge: move left along top
    path.append((x + w - r, y + h))
    path.append((x + r, y + h))
    
    # Top-left arc (from 90° to 180°)
    cx, cy = x + r, y + h - r
    for i in range(segments_per_arc + 1):
        angle = math.pi / 2 + (math.pi / 2) * (i / segments_per_arc)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        path.append((px, py))
    
    # Left edge: move down along left side
    path.append((x, y + h - r))
    path.append((x, y + r))
    
    # Bottom-left arc (from 180° to 270°)
    cx, cy = x + r, y + r
    for i in range(segments_per_arc + 1):
        angle = math.pi + (math.pi / 2) * (i / segments_per_arc)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        path.append((px, py))
    
    # Close the path by returning to start
    path.append((x + r, y))
    
    return path


def create_baseplate_cell_outline(i, j, grid_pitch=42.0, r_baseplate=8.0, segments_per_arc=16):
    """
    Create a 2D outline path for a single baseplate cell.
    
    Args:
        i: Cell index in X direction (0-based)
        j: Cell index in Y direction (0-based)
        grid_pitch: Grid pitch in mm (default 42.0)
        r_baseplate: Corner radius in mm (default 8.0)
        segments_per_arc: Number of segments per quarter-circle (default 16)
    
    Returns:
        List of (x, y) coordinate tuples representing the closed cell outline
        
    Note:
        Each baseplate cell is a rounded rectangle:
        - Located at (i * grid_pitch, j * grid_pitch)
        - Size: grid_pitch × grid_pitch
        - Corner radius: r_baseplate
    """
    cell_origin_x = i * grid_pitch
    cell_origin_y = j * grid_pitch
    
    return create_rounded_rectangle_path(
        x=cell_origin_x,
        y=cell_origin_y,
        w=grid_pitch,
        h=grid_pitch,
        r=r_baseplate,
        segments_per_arc=segments_per_arc
    )


def create_bin_footprint_outline(i, j, nx, ny, grid_pitch=42.0, 
                                 xy_clearance_per_side=0.25, r_bin=3.75, 
                                 segments_per_arc=16):
    """
    Create a 2D outline path for a bin/block footprint spanning multiple cells.
    
    Args:
        i: Starting cell index in X direction (0-based)
        j: Starting cell index in Y direction (0-based)
        nx: Number of cells to span in X direction
        ny: Number of cells to span in Y direction
        grid_pitch: Grid pitch in mm (default 42.0)
        xy_clearance_per_side: Clearance per side in mm (default 0.25)
        r_bin: Corner radius in mm (default 3.75)
        segments_per_arc: Number of segments per quarter-circle (default 16)
    
    Returns:
        List of (x, y) coordinate tuples representing the closed bin footprint
        
    Note:
        A bin spanning (nx, ny) cells placed at grid position (i, j):
        - x = i * grid_pitch + xy_clearance_per_side
        - y = j * grid_pitch + xy_clearance_per_side
        - w = nx * grid_pitch - 2 * xy_clearance_per_side
        - h = ny * grid_pitch - 2 * xy_clearance_per_side
        - r = r_bin (applied only to outermost corners)
    """
    x = i * grid_pitch + xy_clearance_per_side
    y = j * grid_pitch + xy_clearance_per_side
    w = nx * grid_pitch - 2 * xy_clearance_per_side
    h = ny * grid_pitch - 2 * xy_clearance_per_side
    
    return create_rounded_rectangle_path(
        x=x,
        y=y,
        w=w,
        h=h,
        r=r_bin,
        segments_per_arc=segments_per_arc
    )
