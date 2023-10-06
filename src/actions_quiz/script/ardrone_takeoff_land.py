#!/usr/bin/env python

import rospy
import actionlib

from actions_quiz.msg import CustomActionMsgAction, CustomActionMsgGoal, CustomActionMsgResult
from std_msgs.msg import String, Empty



class CustomActionServer(object):
    def __init__(self):
        rospy.init_node('action_custom_msg_as')
        self.server = actionlib.SimpleActionServer('/action_custom_msg_as', CustomActionMsgAction, self.execute, False)
        self.server.start()
        self.feedback_pub = rospy.Publisher('/action_custom_msg_feedback', String, queue_size=1)
        self.takeoff_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self.land_pub = rospy.Publisher('/drone/land', Empty, queue_size=1)


    def execute(self, goal):
        self.takeoff_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self.land_pub = rospy.Publisher('/drone/land', Empty, queue_size=1)
        
        rospy.sleep(1)  # Adjust as needed

        
        
        
        rospy.loginfo("Received goal: %s", goal.goal)

        if goal.goal == 'TAKEOFF':
            
            self.publish_feedback('Taking off...')
            rospy.loginfo("Taking off...")
            self.takeoff_pub.publish(Empty())
        
            rospy.sleep(5)  # Simulating takeoff time
            self.publish_feedback('Takeoff complete!')
        elif goal.goal == 'LAND':
            self.publish_feedback('Landing...')
            # Perform landing logic here
            self.land_pub.publish(Empty())
            rospy.sleep(3)  # Simulating landing time
            self.publish_feedback('Landing complete!')

        self.server.set_succeeded()
    
        '''     # Landing
        self.land_pub.publish(Empty())
        rospy.loginfo("Landing...")
        rospy.sleep(2)  # Adjust as needed
        rospy.loginfo('Succeeded taking off and landing')'''

    def publish_feedback(self, feedback_msg):
        feedback = String()
        feedback.data = feedback_msg
        self.feedback_pub.publish(feedback)

if __name__ == '__main__':
    action_server = CustomActionServer()
    goal = CustomActionMsgGoal()
    goal.goal = 'TAKEOFF'
    action_server.execute(goal)
    goal.goal = 'LAND'
    action_server.execute(goal)
    rospy.spin()