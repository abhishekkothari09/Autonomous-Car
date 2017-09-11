#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from std_msgs.msg import String


		
#Callback function 
def callback(data):
	pose = data
	pose.x = round(pose.x, 4)
	pose.y = round(pose.y, 4)
       	pose.theta=round(pose.theta,4)

def spiral():

	
	#Receiveing the user's input
	aspeed = input("Input your angular speed: ")
	lspeed = input("Input your linear speed: ")
	rte = input("Input your frequency: ")
	max_rad = input("Maximum radius: ")
	
	if aspeed:
		constant_speed = aspeed
	else:
		constane_speed =3
	
	if lspeed:
		rk = lspeed
	else:
		rk = 0.5
	
	if rte:
		ratee=rte
	else:
		ratee=1
		
	if max_rad:
		rad=max_rad
	else:
		rad=5

	#Creating our node,publisher and subscriber
	velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(ratee) #10Hz			
	vel_msg = Twist()
       	pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, callback)
       	pose = Pose()

	decay = 0.5*round((1/ratee),2) # decay calculated based on input rate
	t0 = rospy.Time.now().to_sec() # initial time 
	radius = 0		       #initial radius
	while not rospy.is_shutdown(): # until the publisher is interrupted manually

	
		if radius<rad:         # condition to check if current radius is lesser than input radius
			rk = rk + 1
			
		else:
			constant_speed = constant_speed - decay
			rk = rk - 0.3

	        if constant_speed < 0:  # if angualar velocity goes negative we break the loop
			break

		vel_msg.linear.x = rk
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0

		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		vel_msg.angular.z = constant_speed

		velocity_publisher.publish(vel_msg)		  # publish the velocity msg
		t1=rospy.Time.now().to_sec()	   		  # calculate the current time
		radius = lspeed*(t1-t0)				  # calculate current radius

		print 'Linear Speed =',vel_msg.linear.x
		print 'Angualr speed (theta) =',vel_msg.angular.z
		print 'Rate (frequency) =',ratee
		print 'Current radius =',round(radius,4)
		print '----------------------'
		print '\n'

		rate.sleep()
		
	rospy.spin()

	
if __name__ == '__main__':
	try:
	    spiral()

	except rospy.ROSInterruptException: pass
