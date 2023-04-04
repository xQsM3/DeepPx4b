#!/usr/bin/env python
from __future__ import print_function

import math
import sys,os
import json
import rospy,roslaunch,rospkg
from utils import seg_client,fix_melodic
from sensor_msgs.msg import Image

import pandas as pd
import numpy as np
import dynamic_reconfigure.client

import argparse
from cv_bridge import CvBridge

from utils import visualize,cv_utils,math_utils,kin_utils,geometry_utils
from libs import inf_config
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistStamped
from visualization_msgs.msg import MarkerArray
from utils.ros_com import im_array2im_msg,publish_xypath,DroneStateListener,GoalListener,ImageListener

class Px4Tuner():
    '''
    handles the parameter tuning of px4
    looks up best parameters for current segmentation state,
    and requests ros service to adjust parameters
    '''
    def __init__(self,model_config,labels,dynreconfigure_name):
        rospy.init_node("px4_parameter_tuner")
        self._LUT = self._load_table()
        self._cls_num, self._clss = self._get_clss(model_config)
        self.change_params = dynamic_reconfigure.client.Client(dynreconfigure_name)
        self._labels = self._load_labels(labels)

    def request_parameter_change(self,im):
        params = self._analyze_state(im)
        try:
            config = self.change_params.update_configuration(params)
            print(f"ParamSet successfull: {config}")
        except rospy.ServiceException as e:
            print("failed ParamSet")

    def _analyze_state(self,im):
        print("PARAMETER TUNING")
        print(f"above 50% skyvision in %: {self._class_share(im,0.5)[self._labelID('sky')]}")
        print(f"above 10% skyvision in %: {self._class_share(im,0.1)[self._labelID('sky')]}")
        # analyze segmentation state and suggest px4 parameters
        if self._class_share(im,0.2)[self._labelID("sky")] < 0.8:
            params = self._lookup(3)
        else:
            params = self._lookup(0)

        return params

    def _get_clss(self, model_config_path):
        model_config = inf_config.ConfigArgs(model_config_path)
        cls_num = len(model_config.custom_color) //3
        return cls_num,[i for i in range(0,cls_num)]

    def _class_share(self,im,p):
        strip = self._strip(im,p)
        n = strip.size
        distribution = [np.count_nonzero(strip==c) / n for c in self._clss]
        return distribution

    def _labelID(self,cls_name):
        # returns train id of specific class
        return self._labels[cls_name]["trainID"]
    def _load_labels(self,label_path):
        label_path = inf_config.relative_to_abs_path(label_path)
        with open(label_path) as json_file:
            labels = json.load(json_file)
        return labels
    def _load_table(self):
        lut_path = os.path.join(rospkg.RosPack().get_path("parameter_tuning"),"scripts/lut.csv")
        df = pd.read_csv(lut_path)
        return df

    def _lookup(self,i):
        # looks up best parameters from LUT and stores them in a dictionaryformat for dynamic reconfigure service
        params = dict(zip(self._LUT.loc[i].index,self._LUT.loc[i]))
        return params

    def _strip(self,im,p):
        # crops upper strip of image in percent (p)
        height = im.shape[0]
        height_strip = round(height * p )
        strip = im[0:height_strip,:]
        return strip

def tuning_loop(image_topic, hz,model_config_path,scale,dynreconfigure_name):
    seg_pub = rospy.Publisher("segmentation_image",Image,queue_size=10)
    tune = Px4Tuner(model_config=model_config_path,labels=pargs.labels,dynreconfigure_name=dynreconfigure_name)
    rate = rospy.Rate(hz)
    color_map = visualize.get_color_map(model_config_path)
    im_listener = ImageListener(image_topic)
    while not rospy.is_shutdown():
        # get segmentation
        pred = seg_client.segmentation_client(image_topic,im_listener.im_msg,scale=scale)
        # publish colored segmentation
        pred_colored = visualize.addcolor(pred,color_map)
        im_msg = im_array2im_msg(pred_colored)
        seg_pub.publish(im_msg)
        #calculate new px4 parameters and publish
        tune.request_parameter_change(pred)

        rate.sleep()

def read_rosparams():
    class Args:
        def __init__(self):
            self.dynreconfigure_name = rospy.get_param("px4_parameter_tuner/dynreconfigure_name")
            self.image_topic = rospy.get_param("px4_parameter_tuner/image_topic")
            self.hz = rospy.get_param("px4_parameter_tuner/hz")
            self.scale = rospy.get_param("px4_parameter_tuner/scale")
            self.config = rospy.get_param("px4_parameter_tuner/config")
            self.labels = rospy.get_param("px4_parameter_tuner/labels")
            self.device = rospy.get_param("px4_parameter_tuner/device")
    args = Args()
    return args
if __name__ == "__main__":
    pargs = read_rosparams()
    # start segmentaiton node @todo: change this to launch file
    package = 'segmentation'
    executable = 'seg_service.py'
    node_name = 'segmentation_server'
    node = roslaunch.core.Node(package=package, node_type=executable, name=node_name,args=f"{pargs.config} {pargs.device}")
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    process = launch.launch(node)

    tuning_loop(pargs.image_topic, pargs.hz, pargs.config,pargs.scale,pargs.dynreconfigure_name)
