#! /usr/bin/env python
import rospy
from my_custom_srv_msg_pkg.srv import MyCustomServiceMessage, MyCustomServiceMessageResponse
from geometry_msgs.msg import Twist

rospy.init_node('service_server')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(2)

def my_callback(request):
    rospy.loginfo("BB8 move in circle has been called")
    print("BB8 is moving in a circle")
    duration = request.duration
    
    var = Twist()
    var.linear.x = 0.2
    var.angular.z = 0.2
    
    start_time = rospy.Time.now()
    end_time = start_time + rospy.Duration(duration)
    
    while rospy.Time.now() < end_time and not rospy.is_shutdown():
        pub.publish(var)
        rate.sleep()

    var.linear.x = 0
    var.angular.z = 0
    pub.publish(var)

    response = MyCustomServiceMessageResponse()
    response.success = True
    rospy.loginfo("BB8 move in circle has been terminated")
    
    return response

my_service = rospy.Service('/move_bb8_in_circle_custom', MyCustomServiceMessage, my_callback)

rospy.spin()