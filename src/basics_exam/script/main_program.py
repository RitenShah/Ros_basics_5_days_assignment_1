#!/usr/bin/env python

import rospy
import actionlib
#from std_srvs.srv import Trigger, TriggerRequest
from basics_exam.srv import DistanceMotion, DistanceMotionRequest
from basics_exam.msg import RecordPoseAction, RecordPoseGoal
from geometry_msgs.msg import PoseStamped


# Initialize the ROS node
rospy.init_node('main_program', anonymous=True)

def call_service_server():
    rospy.wait_for_service('/dist_motion_service')
    try:
        # Create a ServiceProxy to call the service
        start_motion_service = rospy.ServiceProxy('/dist_motion_service', DistanceMotion)
        request = DistanceMotionRequest()
        response = start_motion_service(request)
        return response.success
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")
        return False

def main_program():
    
    # Call the Service Server to start drone motion
    success = call_service_server()

    if success=='True':
        rospy.loginfo("Drone motion started successfully.")
        
        # Start the Action Server to record poses
        action_client = actionlib.SimpleActionClient('/rec_pose_as', RecordPoseAction)
        action_client.wait_for_server()

        # Send a goal to the Action Server
        goal = RecordPoseGoal()
        action_client.send_goal(goal)

        # Wait for the action to finish
        action_client.wait_for_result()

        # Get the last recorded pose
        last_pose = action_client.get_last_pose().last_pose
        rospy.loginfo(f"Last recorded pose: {last_pose}")
    else:
        rospy.logerr("Failed to start drone motion.")

if __name__ == '__main__':
   
    try:
        main_program()
    except rospy.ROSInterruptException:
        pass