#!/usr/bin/env python
'''
Developed by Darshan KT
Objective: Sending multiple target poses using ros action client concept
'''

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

waypoints = [[(-1.08, 9.04, 0),(0,0,0.827776247102,0.561058361255)], [(-2.7, 17.04, 0.00498),(0,0, 0.07071067,0.70710678118)]]

def goal_pose(pose):
    goal_pose = MoveBaseGoal()
    goal_pose.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    goal_pose.target_pose.pose.position.x = pose[0][0]
    goal_pose.target_pose.pose.position.y = pose[0][1]
    goal_pose.target_pose.pose.position.z = pose[0][2]
    goal_pose.target_pose.pose.orientation.x = pose[1][0]
    goal_pose.target_pose.pose.orientation.y = pose[1][1]
    goal_pose.target_pose.pose.orientation.z = pose[1][2]
    goal_pose.target_pose.pose.orientation.w = pose[1][3]


if __name__ == '__main__':
    rospy.init_node('patrol')
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    
    while True:
        for pose in waypoints:
            goal = goal_pose(pose)      
            client.send_goal(goal)
            client.wait_for_result()
