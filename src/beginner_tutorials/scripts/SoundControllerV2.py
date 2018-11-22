#!/usr/bin/env python
import rospy 
from beginner_tutorials.msg import *

class SoundControllerV2(object):

    def __init__(self):
        rospy.init_node("soundcontroller", anonymous=True)
        pub = rospy.Publisher("sound", Sound, queue_size=10)
        rate = rospy.Rate(10)
        while rospy.is_shutdown():
            event_id = int(input("EventId:"))
            talk = raw_input("Talk: ")
            angle = int(input("Angle: "))
            pub.publish(eventId=event_id, data=talk, angle=angle)
            rate.sleep()
    


if __name__ == "__main__":
    print ("SoundControllerV2")
    soundcontroller = SoundControllerV2()