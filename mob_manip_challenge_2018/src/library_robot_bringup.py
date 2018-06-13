#!/usr/bin/env python

#Steps 

#1: Keep on checking for pick_gui service
#2: If availble call it and wait for finish: NB: Assume that the book is picked
#3: One finish, send goal position to navigation stack to goto the destination table
#4: Keep on checking whether the pose was successful
#5: If successful, call place
#6: After place, return back to the first table


import rospy

import sys

from std_srvs.srv import Empty
from move_base_msgs.msg import *

#This class comprises of all the functions to do this demo
class Library_Robot:

	def __init__(self):


		#X,y,z and x,y,z,w
		self.table_pose = [-3.33663249016,
				   -1.88953304291,
				    0,

				    0,
				    0,
				    0.997765251106,
				    0.0668169415995]


		rospy.init_node('lib_manager_robot')
		rospy.loginfo("Starting Library Manager Robot interface")



		self.check_service = False
		self.call_pik_service = False
		self.send_goal_service = False
		self.cal_place_service = False
		self.go_home_fn = False



		rospy.Timer(rospy.Duration(1), main_loop)


		self.check_pick_service()


	def main_loop(self,event):
		if(self.check_service):
			self.call_pick_service()

		if(self.call_pik_service):
			self.send_goal_pose()
			




	#Function to check pick gui is available, return true if available
	def check_pick_service(self):

		try:

			rospy.loginfo("Waiting for PICK and Place Services")
			rospy.wait_for_service('pick_gui')
			rospy.loginfo("Pick Gui service is available")
			rospy.wait_for_service('place_gui')
			rospy.loginfo("Place Gui service is available")
			rospy.loginfo("Creating service call for pick and place")
	
			self.pick_service = rospy.ServiceProxy('pick_gui', Empty)
			self.pick_service = rospy.ServiceProxy('place_gui', Empty)

			self.check_service = True

			return 1

		except:
			rospy.logwarn("Exception in Checking PICK and place service")
			sys.exit(0)

		

	#Call Pick service one it available, and return if it is successfull
	def call_pick_service(self):
		try:
			resp = 1

			rospy.loginfo("Calling Pick Service")

			rospy.loginfo("Waiting to be done")


			resp = self.pick_service()
			
			if(resp != 1):
				self.call_pik_service = True
				self.check_service = False

				rospy.loginfo("Picking book completed")


		except:
			rospy.logwarn("Exception in Calling PICK service")
			sys.exit(0)
			
		




	
	#Send goal position to navigation stack once it receive output from pick service, and check it finish or not
	def send_goal_pose(self):
		self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		self.goal_pose = MoveBaseGoal()

		


		rospy.loginfo("Waiting for Move base server")
		self.client.wait_for_server()

	
		self.goal.target_pose.pose.position.x=float(self.table_pose[0])
		self.goal.target_pose.pose.position.y=float(self.table_pose[1])
		self.goal.target_pose.pose.position.z=float(self.table_pose[2])

		self.goal.target_pose.pose.orientation.x = float(self.table_pose[3])
		self.goal.target_pose.pose.orientation.y= float(self.table_pose[4])
		self.goal.target_pose.pose.orientation.z= float(self.table_pose[5])
		self.goal.target_pose.pose.orientation.w= float(self.table_pose[6])

		self.goal.target_pose.header.frame_id= 'map'
		self.goal.target_pose.header.stamp = rospy.Time.now()

		rospy.loginfo("Sending Goal position to the robot")
		self.client.send_goal(self.goal)


	#Once it successfull, call place, return if it is successfull
	def call_place_service(self):
		pass

	#Return back to old place once place is successfull
	def go_home(self):
		pass


if __name__ == "__main__":
	robot_obj = Library_Robot()

	



	

	