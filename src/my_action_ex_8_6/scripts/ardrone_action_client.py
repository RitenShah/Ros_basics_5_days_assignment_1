#! /usr/bin/env python
import rospy
import time
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty

pub= rospy.Publisher('/cmd_vel', Twist, queue_size=1)
takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
takeoff_msg=Empty()
land = rospy.Publisher('/drone/land', Empty, queue_size=1) #Create a Publisher to land the drone
land_msg=Empty()

action_server_name = '/ardrone_action_server'
# waits until the action server is up and running

PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

nImage = 1

var=Twist()
# definition of the feedback callback. This will be called when feedback
# is received from the action server
# it just prints a message indicating a new message has been received
def feedback_callback(feedback):
    global nImage
    print('[Feedback] image n.%d received'%nImage)
    nImage += 1

# initializes the action client node
rospy.init_node('drone_action_client')

# create the connection to the action server
client = actionlib.SimpleActionClient('/ardrone_action_server', ArdroneAction)
rospy.loginfo('Waiting for action Server '+action_server_name)
# waits until the action server is up and running
client.wait_for_server()
rospy.loginfo('Action Server Found...'+action_server_name)


# creates a goal to send to the action server
goal = ArdroneGoal()
goal.nseconds = 10 # indicates, take pictures along 10 seconds

# sends the goal to the action server, specifying which feedback function
# to call when feedback received
client.send_goal(goal, feedback_cb=feedback_callback)

# Uncomment these lines to test goal preemption:
#time.sleep(3.0)
#client.cancel_goal()  # would cancel the goal 3 seconds after starting

# wait until the result is obtained
# you can do other stuff here instead of waiting
# and check for status from time to time 
# status = client.get_state()
# check the client API link below for more info

state_result = client.get_state()

rate = rospy.Rate(1)

rospy.loginfo("state_result: "+str(state_result))

i=0
while not i == 3:
    takeoff.publish(takeoff_msg)
    rospy.loginfo('Taking off...')
    time.sleep(1)
    i += 1

while state_result < DONE:
    rospy.loginfo("Doing Stuff while waiting for the Server to give a result....")
    var.linear.x = 1
    var.angular.z = 1
    pub.publish(var)
    rate.sleep()
    state_result = client.get_state()    
    rospy.loginfo("state_result: "+str(state_result))
    
if state_result == ERROR:
    rospy.logerr("Something went wrong in the Server Side")
if state_result == WARN:
    rospy.logwarn("There is a warning in the Server Side")

i=0
while not i == 3:
    var.linear.x = 0
    var.angular.z = 0
    pub.publish(var)
    land.publish(land_msg)
    rospy.loginfo('Landing...')
    time.sleep(1)
    i += 1

#print('[Result] State: %d'%(client.get_state()))