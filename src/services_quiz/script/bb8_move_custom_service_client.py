#! /usr/bin/env python

import rospy
from services_quiz.srv import BB8CustomServiceMessage, BB8CustomServiceMessageRequest
import sys

# Initialise a ROS node with the name service_client
rospy.init_node('service_client')

start_time = rospy.Time.now()

while rospy.Time.now() - start_time < rospy.Duration(180):
    # Wait for the service client /trajectory_by_name to be running
    rospy.wait_for_service('/move_bb8_in_square_custom')
    # Create the connection to the service
    bb8_move_custom_service = rospy.ServiceProxy('/move_bb8_in_square_custom', BB8CustomServiceMessage)

    # Create an object of type TrajByNameRequest
    bb8_move_custom_object = BB8CustomServiceMessageRequest()

    # Fill the variable traj_name of this object with the desired value
    bb8_move_custom_object.side = 2.0
    bb8_move_custom_object.repetitions = 2

    # Send through the connection the name of the trajectory to be executed by the robot
    result = bb8_move_custom_service(bb8_move_custom_object)

    # Print the result given by the service called
    print(result)

    # Sleep for 3 minutes
    rospy.sleep(2)

    # Set new parameters for the next service call
    bb8_move_custom_object.side = 3.0
    bb8_move_custom_object.repetitions = 1

    # Send through the connection the name of the trajectory to be executed by the robot
    result = bb8_move_custom_service(bb8_move_custom_object)

    # Print the result given by the service called
    print(result)