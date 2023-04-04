import math
import numpy as np

class Point:
    def __init__(self,x,y,z,timestamp):
        self.x = x
        self.y = y
        self.z = z
        self.timestamp = timestamp
class Segment:
    def __init__(self,p1,p2,id):
        self.p1 = p1
        self.p2 = p2
        self.id = id
class Polyline:
    def __init__(self, pol):
        self.polyline_points = []
        for dot in pol:
            self.Add(dot[0],dot[1],dot[2],dot[3])

    def Add(self,x,y,z,timestamp):
        dot = Point(x,y,z,timestamp)
        self.polyline_points.append(dot)

    def build_segments(self):
        segs = []
        for id,(p1,p2) in enumerate(zip(self.polyline_points[:-1],
                                        self.polyline_points[1:])):
            segs.append(Segment(p1,p2,id))
        self.segs = segs
    def connected(self,p,q):
        # check if segment p and q are connected or same segment
        return True if abs(p.id -q.id) <=1 else False
    def SelfIntersections(self):
        self.build_segments()
        present = []
        for p_seg in self.segs:
            for q_seg in self.segs:
                if self.connected(p_seg,q_seg): # skip if segments are connected or equal
                    continue
                p1,p2 = p_seg.p1,p_seg.p2
                q1,q2 = q_seg.p1,q_seg.p2

                detected,isec_point = self.LineIntersects(p1,p2,q1,q2)
                if detected:
                    detection = isec_point[0],isec_point[1],p_seg,q_seg
                    present.append(detection)  # add points to list
        answer = sorted(set(present),key = lambda x: (x[0], x[1]))  # clean list from duplicate points
        return answer  # return list of points

    def SelfApproaches(self,distancethresh,timethresh):
        approaches = []
        #timethresh *= 1000 #miliseconds
        for p in self.polyline_points[1:]:
            for q in self.polyline_points:
                p_array = np.array([p.x,p.y,p.z])
                q_array = np.array([p.x,p.y,p.z])
                geom_distance = np.linalg.norm(p_array - q_array)
                time_distance = abs(p.timestamp-q.timestamp)
                if geom_distance < distancethresh and \
                    time_distance > timethresh:
                    approaches.append([p,q])
        return approaches

    def LineIntersects(self,p1, p2, q1, q2):  # check if intersection present for segment
        s1_x = p2.x - p1.x
        s1_y = p2.y - p1.y
        s2_x = q2.x - q1.x
        s2_y = q2.y - q1.y

        s = (-s1_y * (p1.x - q1.x) + s1_x * (p1.y - q1.y)) / ((-s2_x * s1_y + s1_x * s2_y)+1e-30)
        t = (s2_x * (p1.y - q1.y) - s2_y * (p1.x - q1.x)) / ((-s2_x * s1_y + s1_x * s2_y)+1e-30)

        if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
            intersec_point = self.IntersectionPoint(p1,s1_x,s1_y,t)
            return True,intersec_point
        return False,None

    def IntersectionPoint(self,p1, s1_x, s1_y, t):  # find intersection point for two lines
        i_x = p1.x + (t * s1_x)
        i_y = p1.y + (t * s1_y)
        i_point = i_x, i_y
        return i_point

def postprocess_intersections(intersects,timethresh,z_thresh):
    # this function sorts out intersections which are too close in timestamps or
    # segments are too far in z direction
    #timethresh *= 1000  # miliseconds
    for i in intersects.copy():
        # segments of intersection
        seg_p = i[2]
        seg_q = i[3]
        #if time condition or z condition hurt
        if abs(seg_p.p1.timestamp - seg_q.p1.timestamp) <= timethresh or \
            abs(seg_p.p1.z-seg_q.p1.z) >= z_thresh:
            intersects.remove(i)

    return intersects

