#! /usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyResponse # you import the service message python classes generated from Empty.srv.
from geometry_msgs.msg import Twist 

rospy.init_node('service_server') 


pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
var = Twist()
var.linear.x = 0
var.angular.z = 0
rate = rospy.Rate(2)


def my_callback(request):
    rospy.loginfo("BB8 move in circle has been called")
    print("BB8 is moving in circle")
    var.linear.x=0.5
    var.angular.z=0.5
    pub.publish(var)
    rospy.loginfo("BB8 move in circle has been terminated")
    return EmptyResponse() # the service Response class, in this case EmptyResponse
    #return MyServiceResponse(len(request.words.split())) 


my_service = rospy.Service('/move_bb8_in_circle', Empty, my_callback) # create the Service called my_service with the defined callback

'''if __name__=="__main__":
    while not rospy.is_shutdown():
        var.linear.x=0.5
        var.angular.z=0.5
        pub.publish(var)
        rate.sleep()'''

rospy.spin() # maintain the service open.