#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_demos/license/LICENSE
#

import rospy
import vm_delivery_robot_ctrl 

if __name__ == '__main__':
    rospy.init_node('vm_delivery_robot_ctrl')
    state_manager = vm_delivery_robot_ctrl.StateManager()
    state_manager.loginfo("Initialized")
    state_manager.spin()
    state_manager.loginfo("Bye Bye")