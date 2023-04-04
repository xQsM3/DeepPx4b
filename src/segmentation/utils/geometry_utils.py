#!/usr/bin/env python

import numpy as np
from pyquaternion import Quaternion
from scipy.spatial.transform import Rotation as R

class ROSquaternion(Quaternion):
    # http://wiki.ros.org/tf2/Tutorials/Quaternions
    # ROS represents quaternions in x,y,z,w ..
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    def ros_ori(self):
        # return quaternion in [x,y,z,w] representation for ROS
        return np.array([self.x,self.y,self.z,self.w])

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
            angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            angle_between((1, 0, 0), (1, 0, 0))
            0.0
            angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    z = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

def unit_vector(x):
    return x / np.linalg.norm(x)

def roll_correction(rotation_matrix):
    # sets roll angle to 0 (roll correction)
    r = R.from_matrix(rotation_matrix)
    euler = r.as_euler("xyz")
    euler_corrected = np.concatenate([np.array([0]),euler[1:]],axis=0)
    r = R.from_euler("xyz",euler_corrected)
    return r.as_matrix()

def random_position(low=3,high=200):
    beta = 0.02
    sign = [-1,1]
    pos = np.random.exponential(1/beta,size=(3,))
    pos = np.clip(pos, low, high)
    pos[0] = np.random.choice(sign) * pos[0]
    pos[1] = np.random.choice(sign) * pos[1]

    return pos

def add_noise_to_rotation(rotation_matrix,low=0,high=30):
    # add noise to rotation matrix, between e.g. 0 and 10 degrees euler angles
    beta = 0.05
    sign = [-1, 1]
    noise = np.random.exponential(1/beta,size=(3,))

    noise = np.clip(noise,low,high)
    noise[:2] = np.random.choice(sign,(2,)) * noise[:2]
    #noise[2] = -1 * noise[2]
    r = R.from_matrix(rotation_matrix)
    euler = r.as_euler("zyx",degrees=True)
    euler = euler + noise
    r = R.from_euler("zyx",euler,degrees=True)
    return r.as_matrix()