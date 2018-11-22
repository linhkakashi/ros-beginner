#!/usr/bin/env python
import rospy
from beginner_tutorials.msg import *

class LogicControllerV2:
    def __init__(self, state_controller):
        self.state_controller = state_controller
        self.sound_data = None
        self.angle = 0
        
        rospy.Subscriber("sound", Sound, self.handle_sound)

    
    def handle_sound(self, sound):
        print("LogicControllerV2-handle_sound")
        self.sound_data = sound.data
        self.state_controller.pushToEventQueues(sound.eventId)
