#!/usr/bin/env python

import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import PoseStamped, TransformStamped
import tf2_ros


class GazeboLinkPose:

    def __init__(self, link_name, model_name):
        self.link_name = link_name
        self.link_pose = PoseStamped()
        self.model_name = model_name
        self.br = tf2_ros.TransformBroadcaster()

        if not self.link_name:
            raise ValueError("'link_name' is an empty string")

        self.states_sub = rospy.Subscriber("/gazebo/model_states", ModelStates, self.callback)
        self.pose_pub = rospy.Publisher("/gazebo/" + self.model_name + "/pose", PoseStamped, queue_size = 10)

    def callback(self, data):
        try:
            ind = data.name.index(self.link_name)
            self.link_pose.pose = data.pose[ind]
            self.link_pose.header.frame_id = "/base_link"
            self.link_pose.header.stamp = rospy.Time.now()

            t = TransformStamped()
            t.header.stamp = rospy.Time.now()
            t.header.frame_id = "map" # from
            t.child_frame_id = self.model_name # to
            t.transform.translation = self.link_pose.pose.position
            t.transform.rotation = self.link_pose.pose.orientation
            self.br.sendTransform(t)

        except ValueError:
            pass


if __name__ == '__main__':
    try:
        rospy.init_node('gazebo_link_pose', anonymous=True)
        gp = GazeboLinkPose('heron_0', "ground_truth_heron")
        gp_udrone = GazeboLinkPose('udrone_1', 'ground_truth_udrone')
        publish_rate = rospy.get_param('~publish_rate', 50)

        rate = rospy.Rate(publish_rate)
        while not rospy.is_shutdown():
            gp.pose_pub.publish(gp.link_pose)
            gp_udrone.pose_pub.publish(gp_udrone.link_pose)
            rate.sleep()

    except rospy.ROSInterruptException:
        pass

