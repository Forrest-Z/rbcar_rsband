'''
Developed by Darshan KT
'''

#!/usr/bin/env python
import rospy
import smach
import time
from smach import State, StateMachine
from smach_ros import SimpleActionState, IntrospectionServer
from geometry_msgs.msg import Twist
from math import  pi
import actionlib
from actionlib import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionFeedback
from tf.transformations import quaternion_from_euler
from collections import OrderedDict


class PowerOnRobot(State):
    def __init__(self):
        State.__init__(self, outcomes=['succeeded'])

    def execute(self, userdata):
	rospy.loginfo("Powering ON robot...")
	time.sleep(2)
	return 'succeeded'

class Waiting(State):
    def __init__(self):
        State.__init__(self, outcomes=['succeeded']) 
        
    def execute(self, userdata):
        rospy.loginfo("Calling waiting state")
        time.sleep(10)
        return 'Waiting state succeeded'

   
class main():
    def __init__(self):
    
        rospy.init_node('ware_house', anonymous=False)
        # rospy.on_shutdown(self.shutdown)        
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    	rospy.loginfo("Waiting for move_base action server...")
    	self.move_base.wait_for_server(rospy.Duration(15))
    	rospy.loginfo("Connected to move_base action server")
        self.nav_goal = None
        
        quaternions = list()
    	euler_angles = (pi/2, pi, 3*pi/2, 0)
    	for angle in euler_angles:
		q_angle = quaternion_from_euler(0, 0, angle, axes='sxyz')
		q = Quaternion(*q_angle)
		quaternions.append(q)
     
        self.waypoints = list()
    	self.waypoints.append(Pose(Point(-2.92, 11.8, 0.0025), quaternions[3]))
    	self.waypoints.append(Pose(Point(-2.7, 19.7, 0.0035), quaternions[0]))
    	self.waypoints.append(Pose(Point(12.6, 18.9, 0.0183), quaternions[1]))
	self.waypoints.append(Pose(Point(11.5, 7.17, 0.0121), quaternions[1]))
     
    	room_locations = (('starting_point', self.waypoints[0]),
	              ('loading_point1', self.waypoints[1]),
	              ('loading_point2', self.waypoints[2]),
		          ('unloading_point', self.waypoints[3]))   
     
        
     	self.room_locations = OrderedDict(room_locations)
        nav_states = {}
        
        def smach(self):
            for room in self.room_locations.iterkeys():   
                def nav_goal_cb(userdata, goal):
                    nav_goal = MoveBaseGoal()
                    nav_goal.target_pose.header.frame_id = 'map'
                    nav_goal.target_pose.pose = self.waypoints[room]
                    return nav_goal
                
                move_base_state = SimpleActionState('move_base', MoveBaseAction, goal=self.nav_goal, goal_cb=self.nav_goal_cb, 
                                                    exec_timeout=rospy.Duration(15.0),
                                                    server_wait_timeout=rospy.Duration(10.0))
                nav_states[room] = move_base_state
        
        sm = StateMachine(outcomes=['succeeded','aborted','preempted'])
        
        
        with sm:            
            StateMachine.add('POWER_ON', PowerOnRobot(), transitions={'succeeded':'WAITING'})            
            StateMachine.add('WAITING', Waiting(), transitions={'succeeded':'STARTING'})
            StateMachine.add('STARTING',  nav_states['starting_point'], transitions={'succeeded':'LOADING_POINT','aborted':'LOADING_POINT','preempted':'LOADING_POINT'})
            StateMachine.add('LOADING_POINT',  nav_states['loading_point'], transitions={'succeeded':'UNLOADING_POINT','aborted':'UNLOADING_POINT','preempted':'UNLOADING_POINT'})
            StateMachine.add('UNLOADING_POINT',  nav_states['unloading_point'], transitions={'succeeded':'','aborted':'','preempted':''})

            
            intro_server = IntrospectionServer('restaurant', sm, '/SM_ROOT')
            intro_server.start()
            
            # Execute the state machine
            sm_outcome = sm.execute()      
            intro_server.stop()
                
                
        def shutdown(self):
            rospy.loginfo("Stopping the robot...")
            rospy.sleep(1)
        
     
     
   
    
if __name__ == '__main__':
    try:
        a = main()
        a.smach()
    except rospy.ROSInterruptException:
        rospy.loginfo("Warehouse operation finished")
    