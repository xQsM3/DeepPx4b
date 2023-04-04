#!/usr/bin/env python

from __future__ import print_function
from segmentation.srv import Segmentation
import rospy
import sys
import argparse
from nn.model import NN
from libs import inf_config
import cv2 as cv
from cv_bridge import CvBridge
from utils.fix_melodic import CvBridgeMelodic

from segmentation.msg import SegImage
from sensor_msgs.msg import Image

def handle_segmentation(msg):
    global model

    if CvBridgeMelodic().fix_needed():
        im = CvBridgeMelodic().imgmsg_to_cv2(msg.segimage.image,desired_encoding="bgr8")
    else:
        im = CvBridge().imgmsg_to_cv2(msg.segimage.image,desired_encoding="bgr8")

    if not msg.scale == 1:
        im = cv.resize(im, (0,0), fx=msg.scale, fy=msg.scale)
    pred = model(im)

    # prepare seg message
    seg_msg = SegImage()
    seg_msg.header.stamp = rospy.Time.now()
    seg_msg.image = CvBridge().cv2_to_imgmsg(pred,encoding="passthrough")

    return seg_msg

def segmentation_server():
    seg_serv = rospy.Service("segmentation",Segmentation,handle_segmentation)
    print("segmentation service is ready")
    rospy.spin()



def model_init(pargs):
    # get model config args
    config_args = inf_config.ConfigArgs(pargs.config)
    # get user args
    config_args.device = pargs.device
    # load model with config
    model = NN(config_args)
    print("segmentation model initialized")

    rospy.init_node("segmentation_server",argv=sys.argv,anonymous=False,disable_signals=True,log_level=rospy.INFO)
    sys.argv = rospy.myargv(argv=sys.argv)
    return model

def init():
    class ParserDummy():
        def __init__(self):
            pass
    pargs = ParserDummy()


    try:
        pargs.config = rospy.get_param("/segmentation_server/config")
        pargs.device = rospy.get_param("/segmentation_server/device")
        success = True
    except:
        success = False
    if not success:
        try:
            pargs.config = sys.argv[1]
            pargs.device = sys.argv[2]
        except:
            raise ValueError(usage())

    return model_init(pargs)

def usage():
    return f"args should be [config,device]"

if __name__ == "__main__":
    model = init()
    segmentation_server()

