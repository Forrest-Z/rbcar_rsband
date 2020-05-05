#!/usr/bin/env python
import rospy
from rbcar_navigation.srv import start, startResponse
import os



def callstart(request):

	print(os.system("rosrun rbcar_navigation cmd_to_acker.py" ))
	return stopResponse("Emergency Brake Released")  #stopResponse would be the output responcse object 

rospy.init_node('start_server')
service= rospy.Service('starter', start, callstart)

rospy.spin()