import cv2
import numpy as np

from enum import Enum
import io
import matplotlib
matplotlib.use('agg')  # turn off interactive backend
import matplotlib.pyplot as plt
from libs import inf_config



class Plane(Enum):
    XY = 1
    YX = 1

    XZ = 2
    ZX = 2

    YZ = 3
    ZY = 3

def create_2d_pathplot(path,title,plane=Plane.XY,color="blue"):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    assert plane == Plane.XY # other planes not implemented yet
    if plane == Plane.XY:
        x = [dot.x for dot in path.polyline_points]
        y = [dot.y for dot in path.polyline_points]
        ax.plot(x,y,marker="",color=color)
        plt.title(title)


    #im = plt2arr(fig)
    return fig

def draw_intersections(fig,intersections,color="red"):
    ax = fig.get_axes()[0]
    ax.scatter([a[0] for a in intersections],
                [a[1] for a in intersections],
                marker="o", color=color)
    return fig

def draw_approaches(fig,approaches,color="yellow"):
    ax = fig.get_axes()[0]

    for approach in approaches:
        p,q = approach[0],approach[1],
        ax.plot([p.x,p.y],[q.x,q.y],marker="o",color=color)
    return fig

def plt2arr(fig,draw=True):
    if draw:
        fig.canvas.draw()
    rgba_buf = fig.canvas.buffer_rgba()
    (w,h) = fig.canvas.get_width_height()
    rgba_arr = np.frombuffer(rgba_buf,dtype=np.uint8).reshape((h,w,4))
    rgba_arr = rgba_arr[:,:,0:3]
    bgr_arr = rgba_arr[:,:,::-1]
    return bgr_arr

def addcolor(result, color_map):
    """
    Convert predict result to color image

    Args:
        result (np.ndarray): The predict result of image.
        color_map (list): The color used to save the prediction results.
    Returns:
        colored image
    """

    color_map = [color_map[i:i + 3] for i in range(0, len(color_map), 3)]
    color_map = np.array(color_map).astype("uint8")

    # Use OpenCV LUT for color mapping
    c1 = cv2.LUT(result, color_map[:, 0])
    c2 = cv2.LUT(result, color_map[:, 1])
    c3 = cv2.LUT(result, color_map[:, 2])
    pseudo_img = np.dstack((c3, c2, c1))

    return pseudo_img


def get_color_map_list(num_classes, custom_color=None):
    """
    Returns the color map for visualizing the segmentation mask,
    which can support arbitrary number of classes.

    Args:
        num_classes (int): Number of classes.
        custom_color (list, optional): Save images with a custom color map. Default: None, use paddleseg's default color map.

    Returns:
        (list). The color map.
    """

    num_classes += 1
    color_map = num_classes * [0, 0, 0]
    for i in range(0, num_classes):
        j = 0
        lab = i
        while lab:
            color_map[i * 3] |= (((lab >> 0) & 1) << (7 - j))
            color_map[i * 3 + 1] |= (((lab >> 1) & 1) << (7 - j))
            color_map[i * 3 + 2] |= (((lab >> 2) & 1) << (7 - j))
            j += 1
            lab >>= 3
    color_map = color_map[3:]

    if custom_color:
        color_map[:len(custom_color)] = custom_color
    return color_map

def get_color_map(model_config_path):
    model_config = inf_config.ConfigArgs(model_config_path)
    return get_color_map_list(256, custom_color=model_config.custom_color)