#! /usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from std_srvs.srv import Empty as EmptySrv, EmptyResponse # you import the service message python classes generated from Empty.srv.


rospy.init_node('service_server')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
takeoff = rospy.Publisher('/takeoff', Empty, queue_size=1)

takeoff_msg = Empty()
rate = rospy.Rate(2)
var = Twist()
var.linear.x = 0
var.angular.z = 0



def callback(request):
    i = 0
    while not i == 1:
        takeoff.publish(takeoff_msg)
        rospy.loginfo('Taking off...')
        time.sleep(1)
        i += 1
    
    rospy.sleep(10)

    # Perform square movement logic here
    j=0
    for j in range(4):
        # Move forward
        twist_msg = Twist()
        twist_msg.linear.x = 1  # Adjust as needed
        pub.publish(twist_msg)

        rospy.sleep(1)  # Adjust as needed

        # Stop
        var.linear.x = 0
        var.angular.z = 0
        pub.publish(var)
        
    


        # Move left
        twist_msg.linear.x = 0.0
        twist_msg.angular.z = 0.83  # Adjust as needed
        pub.publish(twist_msg)

        rospy.sleep(2)  # Adjust as needed

        # Stop
        twist_msg.angular.z = 0.0
        pub.publish(twist_msg)

          # Adjust as needed
        j += 1


    response = EmptyResponse()
    rospy.loginfo("Drone move in square has been terminated")
    return response
    
      
    
   

my_service = rospy.Service('/motion_service', EmptySrv, callback)

while not rospy.is_shutdown():
    rate.sleep()

rospy.spin()


