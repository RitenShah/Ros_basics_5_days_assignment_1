#! /usr/bin/env python
import rospy
from services_quiz.srv import BB8CustomServiceMessage, BB8CustomServiceMessageResponse
from geometry_msgs.msg import Twist

rospy.init_node('service_server')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(2)

def my_callback(request):
    rospy.loginfo("BB8 move in square has been called")
    print("BB8 is moving in a square")
    side = request.side
    repetition = request.repetitions
    repetition_2 = 0
    var = Twist()
    start_time = rospy.Time.now()
    end_time = start_time + rospy.Duration(180)
    
    #while rospy.Time.now() < end_time and not rospy.is_shutdown():
    while repetition_2 < repetition:
        side_2 = 0
        print(f"Repetition: {repetition_2}, Side: {side_2}")

        for side_2 in range(4):
            # Move forward
            var.angular.z = 0
            var.linear.x = 0.5
            pub.publish(var)
            rospy.sleep(side / 0.5)

            # Stop
            var.linear.x = 0
            var.angular.z = 0
            pub.publish(var)
            rospy.sleep(1.0)

            # Turn
            var.linear.x = 0
            var.angular.z = 1.57
            pub.publish(var)
            rospy.sleep(1.0)
        
            # Stop
            var.linear.x = 0
            var.angular.z = 0
            pub.publish(var)
            rospy.sleep(1.0)

            side_2 += 1
            print(f"Repetition: {repetition_2}, Side: {side_2}")

        repetition_2 += 1

    response = BB8CustomServiceMessageResponse()
    response.success = True
    rospy.loginfo("BB8 move in square has been terminated")
    print(response)
    
    var.linear.x = 0
    var.angular.z = 0
    pub.publish(var)

    
    
    return response

my_service = rospy.Service('/move_bb8_in_square_custom', BB8CustomServiceMessage, my_callback)
rospy.spin()