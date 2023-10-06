#!/usr/bin/env python


import rospy
# Import the service message used by the service /trajectory_by_name
from std_srvs.srv import Empty, EmptyRequest

# Initialise a ROS node with the name service_client
rospy.init_node('service_client')
# Wait for the service client /trajectory_by_name to be running
rospy.wait_for_service('/move_bb8_in_circle')
# Create the connection to the service
bb8_circle_robot = rospy.ServiceProxy('/move_bb8_in_circle', Empty)
# Create an object of type TrajByNameRequest
bb8_circle_robot_object = EmptyRequest()
bb8_circle_robot(bb8_circle_robot_object)
'''result=bb8_circle_robot(bb8_circle_robot_object)
# Print the result given by the service called
print(result)'''
#file_path = 'path/to/file.txt'
#file_string = read_file_as_string(file_path)