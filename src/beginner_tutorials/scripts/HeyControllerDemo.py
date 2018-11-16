#!/usr/bin/env python
import rospy 
from std_msgs.msg import String 

def talker():
    pub = rospy.Publisher("chatter", String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)

    while 1:
        a = raw_input("Demo speech: ")
        pub.publish(a)
        #rate.sleep()

if __name__ == "__main__":
    print ("Hello")
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
