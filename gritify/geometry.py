"""Base geometry utilities for Gridfinity structures."""

import numpy as np
from stl import mesh


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
