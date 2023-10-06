#!/usr/bin/env python

import rospkg
rospack = rospkg.RosPack()
# This rospack.get_path() works in the same way as $(find name_of_package) in the launch files.
traj = rospack.get_path('iri_wam_reproduce_trajectory') + "/config/get_food.txt"

import rospy
# Import the service message used by the service /trajectory_by_name
from iri_wam_reproduce_trajectory.srv import ExecTraj, ExecTrajRequest


# Initialise a ROS node with the name service_client
rospy.init_node('service_client')
# Wait for the service client /trajectory_by_name to be running
rospy.wait_for_service('/execute_trajectory')
# Create the connection to the service
exec_traj_service = rospy.ServiceProxy('/execute_trajectory', ExecTraj)
# Create an object of type TrajByNameRequest
exec_traj_object = ExecTrajRequest()
exec_traj_object.file=traj
result=exec_traj_service(exec_traj_object)
# Print the result given by the service called
print(result)
#file_path = 'path/to/file.txt'
#file_string = read_file_as_string(file_path)