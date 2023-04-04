#!/usr/bin/env python

import rospy

from dynamic_reconfigure.server import Server
from parameter_tuning.cfg import ParameterTunerNodeConfig

def callback(config, level):
	rospy.loginfo("""Reconfigure Request: {}""".format(config))
	return config

if __name__ == "__main__":
	rospy.init_node("parameter_tuner_node", anonymous = False)

	src = Server(ParameterTunerNodeConfig, callback)
	rospy.spin()

