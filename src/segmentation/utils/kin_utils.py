import numpy as np

class Pose:
    def __init__(self,x,y,z):
        self._x = x
        self._y = y
        self._z = z
    @property
    def pos_asarray(self):
        return np.array([self._x,self._y,self._z])
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,x):
        self._x = x
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self,y):
        self._y = y
    @property
    def z(self):
        return self._z
    @z.setter
    def z(self,z):
        self._z = z

class Velocity(Pose):
    def __init__(self,x,y,z):
        super().__init__(x,y,z)
