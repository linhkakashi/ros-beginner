#!/usr/bin/env python

import sys
import rospy
import threading

import smach
from smach import StateMachine
from smach_ros import ServiceState, SimpleActionState

from beginner_tutorials.srv import *

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        resp1 = add_two_ints(x, y)
        return resp1.sum
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

class IDLE(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=["hey", "none"])

  def execute(self, userdata):
    rospy.loginfo("Executing state IDLE")
    return "hey"

class Hey(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=["ready_to_move"])

  def execute(self, userdata):
    rospy.loginfo("Executing state Hey")
    x = int(input("input x: "))
    y = int(input("input y: "))
    add_two_ints_client(x, y)

    return "ready_to_move"


class Ready(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=["come_here", "idle", "stop"])
    self.count = 1

  def execute(self, userdata):
    rospy.loginfo("Executing state Ready")
    if self.count == 1:
      self.count += 1
      return "come_here"
    elif self.count < 3:
      self.count += 1
      return "idle"
    else:
      return "stop"

class Approach(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=["done"])

  def execute(self, userdata):
    rospy.loginfo("Executing state Approach")
    return "done"

def main():
  rospy.init_node('smach_example_state_machine')

  sm = smach.StateMachine(outcomes=["stop"])

  with sm:
    smach.StateMachine.add("IDLE", IDLE(),
      transitions={"hey":"HEY", "none": "IDLE"})
    smach.StateMachine.add('HEY', Hey(),
      transitions={"ready_to_move":"READY"})
    smach.StateMachine.add("READY", Ready(),
      transitions={"come_here": "APPROACH",
                   "idle": "IDLE",
                   "stop": "stop"})
    smach.StateMachine.add("APPROACH", Approach(),
      transitions={"done": "READY"})
  outcome = sm.execute()


if __name__ == '__main__':
    main()

