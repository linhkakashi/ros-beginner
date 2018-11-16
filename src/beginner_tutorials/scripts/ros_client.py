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
#    x = int(input("input x: "))
#    y = int(input("input y: "))
    add_two_ints_client(1, 2)

    return "ready_to_move"

class Hey2(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=["hey2"])
  
  def execute(self, userdata):
    rospy.loginfo("Executing state Hey2")
    add_two_ints_client(2, 4)
    
    #time.sleep(10)
    return "hey2"
  

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

class End(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=["end"])
  def execute(self, userdata):
    rospy.loginfo("Executing state END")
    return "end"

def main():
  rospy.init_node('smach_example_state_machine')

  sm = smach.StateMachine(outcomes=["stop"])

  with sm:
    smach.StateMachine.add("IDLE", IDLE(),
      transitions={"hey":"CON", "none": "IDLE"})
    sm_con = smach.Concurrence(outcomes=['outcome4','outcome5'],
      default_outcome='outcome4',
      outcome_map={'outcome5':{ 'HEY':'ready_to_move', 'HEY2':'hey2'}})
   
    with sm_con:
      smach.Concurrence.add('HEY', Hey())
      smach.Concurrence.add('HEY2', Hey2())
    
    smach.StateMachine.add('CON', sm_con,
     transitions={'outcome4':'END', 'outcome5':'READY'})
    smach.StateMachine.add("END", End(),
      transitions={"end": "stop"})
    smach.StateMachine.add("READY", Ready(),
      transitions={"come_here": "APPROACH",
                   "idle": "IDLE",
                   "stop": "stop"})
    smach.StateMachine.add("APPROACH", Approach(),
      transitions={"done": "READY"})
  outcome = sm.execute()


if __name__ == '__main__':
    main()

