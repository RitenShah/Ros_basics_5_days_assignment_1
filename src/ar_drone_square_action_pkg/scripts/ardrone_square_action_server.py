#!/usr/bin/env python
import rospy
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import time

rospy.init_node('ardrone')


class ArdroneClass(object):
    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.takeoff_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self.land_pub = rospy.Publisher('/drone/land', Empty, queue_size=1)

        self._as = actionlib.SimpleActionServer("ardrone_as", ArdroneAction, self.goal_callback, False)
        
    
    def goal_callback(self, goal):
        self.takeoff_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self.land_pub = rospy.Publisher('/drone/land', Empty, queue_size=1)
        
        rospy.sleep(1)  # Adjust as needed

        r = rospy.Rate(1)
        success = True
        # self.current_goal = self._as.accept_new_goal()

        rospy.loginfo("Taking off...")
        self.takeoff_pub.publish(Empty())
        rospy.sleep(3)  # Adjust as needed

        # publish info to the console for the user
        rospy.loginfo('"ardrone_as": Executing, flying in square')

        i = 0
        # Perform square movement logic here
        for i in range(4):
            # Move forward
            twist_msg = Twist()
            twist_msg.linear.x = 1.0  # Adjust as needed
            self.pub.publish(twist_msg)

            rospy.sleep(1)  # Adjust as needed

            # Move right
            twist_msg.linear.x = 0.0
            twist_msg.angular.z = -1.570796325  # Adjust as needed
            self.pub.publish(twist_msg)

            rospy.sleep(1)  # Adjust as needed

            # Stop
            twist_msg.angular.z = 0.0
            self.pub.publish(twist_msg)

            rospy.sleep(1)  # Adjust as needed
            i += 1
            if self._as.is_preempt_requested():
                rospy.loginfo('The goal has been cancelled/preempted')
                # The following line sets the client in preempted state (goal cancelled)
                self._as.set_preempted()
                success = False
                # We end the square movement
                break

        # End of square movement logic

        # Landing
        self.land_pub.publish(Empty())
        rospy.loginfo("Landing...")
        rospy.sleep(3)  # Adjust as needed
        rospy.loginfo('Succeeded flying in a square')
        
        '''if success:
            rospy.loginfo('Succeeded flying in a square')
            result = ArdroneResult()  # Assuming ArdroneResult is defined
            self._as.set_succeeded(result)'''

if __name__ == '__main__':
    drone_node = ArdroneClass()
    drone_node.goal_callback(None)
    rospy.spin()

