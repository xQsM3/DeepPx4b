import cv2 as cv
import numpy as np

def boolean_mask_from_cls_mask(cls_mask: np.ndarray,
                               cls_id: np.ndarray) ->np.ndarray:
    bool_mask = cls_mask.copy()
    bool_mask[bool_mask==255] = 999 # no class found
    bool_mask[bool_mask==cls_id] = 255
    bool_mask[bool_mask!=255] = 0
    return bool_mask
def erode(mask: np.ndarray) -> np.ndarray:
    kernel = np.ones((3, 3), np.uint8)
    mask = cv.erode(mask,kernel,iterations=40)
    return mask
def corners(mask):
    c = np.zeros(mask.shape)
    harris_corners = cv.cornerHarris(mask, 3, 3, 0.05)
    kernel = np.ones((7, 7), np.uint8)
    harris_corners = cv.dilate(harris_corners, kernel, iterations=2)
    c[harris_corners > 0.025 * harris_corners.max()] = 255
    c = c.astype(int)
    return c


def edges(mask):
    return cv.Canny(mask,100,200)

def contours(mask):
    contours,_ = cv.findContours(mask,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    return contours

def box_contours(contours):
    boxes = [cv.boundingRect(c) for c in contours]
    boxes = np.asarray(boxes)
    return boxes # list of [[x,y,w,h]]