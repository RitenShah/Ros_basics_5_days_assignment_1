#! /usr/bin/env python

import rospy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan             


# Initiate a Node named 'topics_quiz_node'
rospy.init_node('topics_quiz_node')

                                          
# Set a publish rate of 2 Hz
rate = rospy.Rate(2)

var = Twist()
var.linear.x = 0
var.angular.z = 0

def callback(msg):
    if msg.ranges[360]>1:
        var.linear.x = 0.6
        var.angular.z = 0
    elif msg.ranges[360]<1:
        var.linear.x = 0
        var.angular.z = 0.2
    elif msg.ranges[360]>1 and msg.ranges[0]>1:
        var.linear.x = 0.6
        var.angular.z = 0
    if msg.ranges[0]<1:
        var.linear.x = 0
        var.angular.z = 0.2
    if msg.ranges[719]<1:
        var.linear.x = 0
        var.angular.z = -1
    pub.publish(var)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)    
sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, callback) 


while not rospy.is_shutdown(): 
    rate.sleep()
