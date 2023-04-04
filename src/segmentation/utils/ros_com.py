from utils import seg_client,fix_melodic
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from utils import visualize,cv_utils,math_utils,kin_utils,geometry_utils
import rospy
def im_array2im_msg(im_array):
    if fix_melodic.CvBridgeMelodic().fix_needed():
        im_msg = fix_melodic.CvBridgeMelodic().cv2_to_imgmsg(im_array, encoding="bgr8")
    else:
        im_msg = CvBridge().cv2_to_imgmsg(im_array, encoding="passthrough")
    return im_msg

def publish_xypath(path ,intersects ,approaches ,stucked):

    pub = rospy.Publisher("xy_path_intersections", Image, queue_size=10)
    fig = visualize.create_2d_pathplot(path, title=f"XY PATH [detected intersects in red]\n"
                                                   f"stucked: {stucked != 0}")
    fig = visualize.draw_intersections(fig, intersects ,color="red")
    fig = visualize.draw_approaches(fig, approaches ,color="yellow")
    plot_img = visualize.plt2arr(fig)
    im_msg = im_array2im_msg(plot_img)
    pub.publish(im_msg)

class DroneStateListener:
    def __init__(self,pose_topic,pose_type,vel_topic,vel_type):
        rospy.Subscriber(pose_topic,pose_type,self.pose_callback) #from nav_msgs.msg import Odometry
        self.pose_msg = rospy.wait_for_message(pose_topic,pose_type,timeout=20)

        rospy.Subscriber(vel_topic,vel_type,self.vel_callback) #from nav_msgs.msg import Odometry
        self.vel_msg = rospy.wait_for_message(vel_topic,vel_type,timeout=20)
        #"/mavros/local_position/velocity_local"
    @property
    def pos(self):
        x = self.pose_msg.pose.pose.position.x
        y = self.pose_msg.pose.pose.position.y
        z = self.pose_msg.pose.pose.position.z
        pos = kin_utils.Pose(x,y,z)
        return pos

    @property
    def vel_linear(self):
        x = self.vel_msg.twist.linear.x
        y = self.vel_msg.twist.linear.y
        z = self.vel_msg.twist.linear.z
        vel = kin_utils.Velocity(x, y, z)
        return vel

    def pose_callback(self,msg):
        self.pose_msg = msg
    def vel_callback(self,msg):
        self.vel_msg = msg

class GoalListener:
    def __init__(self,goal_topic,type):
        rospy.Subscriber(goal_topic,type,self.pose_callback)
        self.pose_msg = rospy.wait_for_message(goal_topic,type,timeout=20)
    @property
    def pos(self):
        x = self.pose_msg.markers[0].pose.position.x
        y = self.pose_msg.markers[0].pose.position.y
        z = self.pose_msg.markers[0].pose.position.z
        pos = kin_utils.Pose(x,y,z)
        return pos

    @property
    def vel_linear(self):
        x = self.vel_msg.twist.linear.x
        y = self.vel_msg.twist.linear.y
        z = self.vel_msg.twist.linear.z
        vel = kin_utils.Velocity(x, y, z)
        return vel

    def pose_callback(self,msg):
        self.pose_msg = msg
    def vel_callback(self,msg):
        self.vel_msg = msg

class ImageListener:
    def __init__(self,image_topic):
        rospy.Subscriber(image_topic,Image,self.callback)
        self.im_msg = rospy.wait_for_message(image_topic,Image,timeout=20)
    def callback(self,im_msg):
        self.im_msg = im_msg