#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import rospy,rospkg
from segmentation.srv import *
from segmentation.msg import SegImage
from sensor_msgs.msg import Image

import cv2 as cv
from cv_bridge import CvBridge
from utils.fix_melodic import CvBridgeMelodic


def segmentation_client(image_topic):
    # get image from drone camera
    im_msg = rospy.wait_for_message(image_topic, Image,timeout=20)

    #im = cv.imread("/home/xqsme/Pictures/test2.png")
    #im_msg = CvBridge().cv2_to_imgmsg(im,encoding="bgr8")
    seg_msg = SegImage()
    seg_msg.image = im_msg
    seg_msg.header.stamp = rospy.Time.now()
    rospy.wait_for_service("segmentation",timeout=20)

    try:
        seg = rospy.ServiceProxy("segmentation",Segmentation)
        pred_msg = seg(seg_msg) # get segmentation from seg model service
        if CvBridgeMelodic().fix_needed():
            pred = CvBridgeMelodic().imgmsg_to_cv2(pred_msg.segimage.image, desired_encoding="passthrough")
        else:
            pred = CvBridge().imgmsg_to_cv2(pred_msg.segimage.image, desired_encoding="passthrough")
        return pred
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return f"args should be [image_topic]"

if __name__ == "__main__":
    if len(sys.argv) == 2:
        image_topic = sys.argv[1]
    else:
        raise ValueError(usage())
    rospy.init_node("segmentation_client")
    segmentation_client(image_topic)




