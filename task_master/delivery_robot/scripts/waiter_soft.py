#!/usr/bin/env python
import rospy
import threading
import random
import time

##ros msg
import actionlib
from cafe_msgs.msg import *

class WaiterSoftBot(object):
    def __init__(self,robot_name,action_name):
        self.name = robot_name
        self.action_name = action_name
        self.waiter_server = actionlib.SimpleActionServer(self.action_name,DeliverOrderAction, execute_cb = self.execute_callback,auto_start=False)
        
    def spin(self):
        self.waiter_server.start() 
        rospy.loginfo("Waiterbot has been Started")
        rospy.spin()

    def process_status(self,time_range,message,feedback_status):
        k = 0;
        timeout = random.randrange(time_range[0],time_range[1])
        while k < timeout and not rospy.is_shutdown():
            k += 1
            rospy.sleep(1)
            rospy.loginfo(self.name + " : " +  message +", [%d/%d]"%(k,timeout))
        
        feedback = DeliverOrderFeedback()
        feedback.status = feedback_status
        self.waiter_server.publish_feedback(feedback)

    def execute_callback(self,data):
        #print data, type(data), dir(data)
        #print type(data._connection_header)
        rospy.loginfo("Order Received : Robotname = %s",data.order.robot_name)

        #Go to kitchen, and return feedback ARRIVE_KITCHEN
        self.process_status(time_range=[5,10],message="GO_TO_KITCHEN",feedback_status=Status.ARRIVE_KITCHEN)

        # Waiting for kitchen
        feedback = DeliverOrderFeedback()
        feedback.status = Status.WAITING_FOR_KITCHEN    
        self.waiter_server.publish_feedback(feedback)
        
        #Wait for kitchen     
        self.process_status(time_range=[1,3],message="WAITING_FOR_KITCHEN",feedback_status=Status.IN_DELIVERY)
        
        #In delivery      
        self.process_status(time_range=[10,20],message="IN_DELIEVERY",feedback_status=Status.ARRIVE_TABLE)
        rospy.loginfo(self.name + " : ARRIVE_TABLE")
        
        # Waiting for user confirmation
        feedback = DeliverOrderFeedback()
        feedback.status = Status.WAITING_FOR_USER_CONFIRMATION    
        self.waiter_server.publish_feedback(feedback)
        
        self.process_status(time_range=[10,15],message="WAITING FOR USER CONFIRMATION",feedback_status=Status.COMPLETE_DELIEVERY)
        rospy.loginfo(self.name + " : COMPLETE_DELIEVERY")
        
        feedback = DeliverOrderFeedback()
        feedback.status = Status.RETURNING_TO_DOCK    
        self.waiter_server.publish_feedback(feedback)
        
        # Returning to Docking
        self.process_status(time_range=[20,30],message="RETURNING TO DOCK", feedback_status=Status.END_DELIEVERY_ORDER)
        rospy.loginfo(self.name+ " : END_DELIEVERY_ORDER")
		
        rospy.sleep(1)
        
        # Closing off the delivery 
        result = DeliverOrderResult("Success!")
        self.waiter_server.set_succeeded(result)

    
if __name__ == '__main__':
    
    try:
        # Initialize ros node
        rospy.init_node('waiterbot')

        waiter = WaiterSoftBot(rospy.get_name(),"~delivery_order")
        rospy.loginfo('Initialized')

        waiter.spin()
        rospy.loginfo("Bye Bye")

    except rospy.ROSInterruptException:
        pass

