#!/usr/bin/env python

import rospy
import actionlib
from basics_exam.msg import RecordPoseAction, RecordPoseResult
from nav_msgs.msg import Odometry


rospy.init_node("check_distance_action_server")
rate=rospy.Rate(1)

class CheckDistanceActionServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer("/rec_pose_as", RecordPoseAction, self.execute, False)
        self.poses = []

        # Subscribe to the odometry topic
        self.odom_sub = rospy.Subscriber("/ground_truth/state", Odometry, self.pose_callback)

    def pose_callback(self, msg):
        # Extract the position from Odometry and store it
        pose = msg.pose.pose
        self.poses.append(pose)
    
    def get_last_pose(self):
        # Get the last recorded pose
        if self.poses:
            return self.poses[-1]
        else:
            return None

    def execute(self, goal):
        # Your action server logic here
        rospy.loginfo("Recording positions for 20 seconds...")
        
        i=0

        for i in range(20):
            self.odom_sub = rospy.Subscriber("/ground_truth/state", Odometry, self.pose_callback)
            rate.sleep()
            i+=1
        rospy.loginfo("Waiting for 60 seconds...")
        # Wait for 60 seconds (adjust as needed)
        #rospy.sleep(20)

        # Provide the list of poses as the result
        result = RecordPoseResult()
        result.poses[:]=self.poses[:]
        self.server.set_succeeded(result)
        rospy.loginfo("Recording completed.")
        print(len(self.poses))
if __name__ == "__main__":
    
    server = CheckDistanceActionServer()
    server.server.start()
    while not rospy.is_shutdown(): 
        rate.sleep()

