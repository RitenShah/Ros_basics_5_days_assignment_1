#!/usr/bin/env python
import rospy
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback

def feedback_callback(feedback):
    print('[Feedback] Flying in square...')

def ardrone_action_client():
    rospy.init_node('ardrone_action_client')

    # Create an action client
    client = actionlib.SimpleActionClient('ardrone_as', ArdroneAction)

    # Wait until the action server is up and running
    rospy.loginfo('Waiting for action server...')
    client.wait_for_server()
    rospy.loginfo('Action server is up!')

    # Create a goal
    goal = ArdroneGoal()

    # Send the goal to the action server and specify the feedback callback
    client.send_goal(goal, feedback_cb=feedback_callback)

    # Uncomment these lines to test goal preemption:
    # time.sleep(3.0)
    # client.cancel_goal()  # would cancel the goal 3 seconds after starting

    # Wait until the result is obtained
    # You can do other stuff here instead of waiting and check for status from time to time
    state_result = client.get_state()
    rospy.loginfo("Waiting for result...")

    while state_result < ArdroneGoal.DONE:
        rospy.sleep(1)
        state_result = client.get_state()
        rospy.loginfo("Current state: {}".format(state_result))

    if state_result == ArdroneGoal.ERROR:
        rospy.logerr("Something went wrong in the Server Side")
    if state_result == ArdroneGoal.WARN:
        rospy.logwarn("There is a warning in the Server Side")

    # Shutdown the client
    client.cancel_all_goals()
    rospy.loginfo("Shutting down the client.")

if __name__ == '__main__':
    try:
        ardrone_action_client()
    except rospy.ROSInterruptException:
        rospy.logerr("Program interrupted before completion.")