#!/usr/bin/env python
'''
Developed by Darshan KT
Objective: Sending target pose using ros action client concept
'''

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def movebase_client():
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	client.wait_for_server()

	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
	goal.target_pose.pose.position.x = 9.21
	goal.target_pose.pose.position.y = 16.4
	# goal.target_pose.pose.position.z = 0.00159
	goal.target_pose.pose.orientation.z = -0.729
	goal.target_pose.pose.orientation.w = 0.689 

	client.send_goal(goal)
	client.wait_for_result()




if __name__ == '__main__':
	try:
		rospy.init_node('movebase_client')
		result = movebase_client()
		if result:
			rospy.loginfo("Goal execution done!")

	except rospy.ROSInterruption:
		rospy.loginfo('Navigation test finished')