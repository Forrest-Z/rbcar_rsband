#!/usr/bin/env python
# Note: Refer this website for more information https://www.theconstructsim.com/ros-mini-challenge-6-detect-the-position-of-a-robot-using-ros-service/
'''
Developed by Darshan KT
Objective: Applying Emergency brake using rosservice concept
'''

import rospy
from rbcar_navigation.srv import stop, stopResponse
import os



def callstop(request):                    #any string request data is enough to execute the below callstop server body
    nodes = os.popen("rosnode list").readlines()
    for i in range(len(nodes)):
    	nodes[i] = nodes[i].replace("\n", "")
    	# print(nodes[i])

    for node in nodes:
    	# print(node)
    	if node == "/cmd_vel_to_ackermann_drive":
    		# print(node)
    		print(os.system("rosnode kill /cmd_vel_to_ackermann_drive" ))
    		break

    return stopResponse("Emergency Brake Applied")  #stopResponse would be the output responcse object 

rospy.init_node('service_server')
service= rospy.Service('stopper', stop, callstop)

rospy.spin()