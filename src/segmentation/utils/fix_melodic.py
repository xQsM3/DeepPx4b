import numpy as np
import subprocess
from cv_bridge import CvBridge,CvBridgeError
import sensor_msgs

class CvBridgeMelodic(CvBridge):
    # CvBridge version 1.13 (melodic ros) is broken for python3, theirfore we need to fix it here
    def __init__(self):
        super().__init__()
    def imgmsg_to_cv2(self, img_msg, desired_encoding = "passthrough"):
        assert desired_encoding == "passthrough" or desired_encoding == "bgr8" or desired_encoding == "rgb8" #this melodic fix is only implemented for rgb8,bgr8,passthrough

        im = np.frombuffer(img_msg.data, dtype=np.uint8).reshape(img_msg.height, img_msg.width, -1)

        if desired_encoding != "passthrough" and desired_encoding != img_msg.encoding:
            im = im[..., ::-1].copy() # convert bgr in rgb or vice versa

        return im

    def cv2_to_imgmsg(self, cvim, encoding = "passthrough"):
        """
        Convert an OpenCV :cpp:type:`cv::Mat` type to a ROS sensor_msgs::Image message.

        :param cvim:      An OpenCV :cpp:type:`cv::Mat`
        :param encoding:  The encoding of the image data, one of the following strings:

           * ``"passthrough"``
           * one of the standard strings in sensor_msgs/image_encodings.h

        :rtype:           A sensor_msgs.msg.Image message
        :raises CvBridgeError: when the ``cvim`` has a type that is incompatible with ``encoding``

        If encoding is ``"passthrough"``, then the message has the same encoding as the image's OpenCV type.
        Otherwise desired_encoding must be one of the standard image encodings

        This function returns a sensor_msgs::Image message on success, or raises :exc:`cv_bridge.CvBridgeError` on failure.
        """
        import cv2
        import numpy as np
        if not isinstance(cvim, (np.ndarray, np.generic)):
            raise TypeError('Your input type is not a numpy array')
        img_msg = sensor_msgs.msg.Image()
        img_msg.height = cvim.shape[0]
        img_msg.width = cvim.shape[1]
        if len(cvim.shape) < 3:
            cv_type = self.dtype_with_channels_to_cvtype2(cvim.dtype, 1)
        else:
            cv_type = self.dtype_with_channels_to_cvtype2(cvim.dtype, cvim.shape[2])
        if encoding == "passthrough":
            img_msg.encoding = cv_type
        else:
            img_msg.encoding = encoding
            # Verify that the supplied encoding is compatible with the type of the OpenCV image
            #if self.cvtype_to_name[self.encoding_to_cvtype2(encoding)] != cv_type:
            #    r = self.cvtype_to_name[self.encoding_to_cvtype2(encoding)]
            #    raise CvBridgeError("encoding specified as %s, but image has incompatible type %s" % (encoding, cv_type))

        if cvim.dtype.byteorder == '>':
            img_msg.is_bigendian = True
        img_msg.data = cvim.tostring()
        img_msg.step = len(img_msg.data) // img_msg.height

        return img_msg

    def fix_needed(self):
        new_proc = subprocess.Popen(["rosversion", "-d"], stdout=subprocess.PIPE)
        version_str = str(new_proc.communicate()[0]).split("'")[1][:-2]
        return version_str == "melodic"