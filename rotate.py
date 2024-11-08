import numpy as np
import math

# Rotation matrix for the Z-axis
def rotate_z(angle):
    angle_rad = math.radians(angle)
    cos_theta = np.cos(angle_rad)
    sin_theta = np.sin(angle_rad)
    
    return np.array([
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0, 0, 1]
    ])

# Rotation matrix for the X-axis
def rotate_x(angle):
    angle_rad = math.radians(angle)
    cos_theta = np.cos(angle_rad)
    sin_theta = np.sin(angle_rad)
    
    return np.array([
        [1, 0, 0],
        [0, cos_theta, -sin_theta],
        [0, sin_theta, cos_theta]
    ])

# Rotation matrix for the Y-axis
def rotate_y(angle):
    angle_rad = math.radians(angle)
    cos_theta = np.cos(angle_rad)
    sin_theta = np.sin(angle_rad)
    
    return np.array([
        [cos_theta, 0, sin_theta],
        [0, 1, 0],
        [-sin_theta, 0, cos_theta]
    ])

def rotate_vertices(vertices, rotation_matrix):
    rotated_vertices = []
    for vertex in vertices:
        rotated_vertex = np.dot(rotation_matrix, np.array(vertex))
        rotated_vertices.append(rotated_vertex)
    return rotated_vertices
