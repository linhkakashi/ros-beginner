#!/usr/bin/env python

import sys
import rospy
import threading
from concurrent.futures import ThreadPoolExecutor
import smach
import time
from smach import StateMachine
from smach_ros import ServiceState, SimpleActionState
import beginner_tutorials.srv
from beginner_tutorials.srv import *

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        resp1 = add_two_ints(x, y)
        return resp1.sum
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

class StateController:
  def __init__(self):
    print("initStateController")

  def listenerHey(self):
    while True:
      x = raw_input("Listening... , Please say: ")
      if x == "hey":
        return "done"
      elif x == "error":
        return "error"
  
  def inactiveSound(self):
    print("InactiveSound")
    time.sleep(2)
    print("Done inactive Sound")
    return "done"
  
  def determineDirection(self):
    print("determineDirection")
    time.sleep(5)
    print("Done determineDirection")
    return "done"
  
  def moveToTarget(self):
    print("moveToTarget")
    time.sleep(30)
    print("Done moveToTarget")
    return "done"


stateController = StateController()

class IDLE(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=["to_active", "none"])

  def execute(self, userdata):
    rospy.loginfo("Executing state IDLE")
    result = stateController.listenerHey()
    if result == "done":
      return "to_active"
    return "none"
def oke():
  print("Executing oke")
  time.sleep(10)
  return "done"

class Activation(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=["ready_to_move"])

  def execute(self, userdata):
    rospy.loginfo("Executing state Hey")
    executor = ThreadPoolExecutor(max_workers=3)
    soundInactive = executor.submit(stateController.inactiveSound)
    determineDirection = executor.submit(stateController.determineDirection)
    moveToTarget = executor.submit(stateController.moveToTarget)
    # soundInactive = executor.submit(oke)
    # determineDirection = executor.submit(oke)
    # moveToTarget = executor.submit(oke)
    if soundInactive.result() == "done" and determineDirection.result() == "done" and moveToTarget.result() == "done":
      return "ready_to_move"
    else:
      print("Erorrrrrrrrrrrrrrrrrrrrrrrrrrrr")
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
      transitions={"to_active":"ACTIVATION", "none": "IDLE"})
    smach.StateMachine.add('ACTIVATION', Activation(),
      transitions={"ready_to_move":"READY"})
    smach.StateMachine.add("READY", Ready(),
      transitions={"come_here": "APPROACH_SERVICE",
                   "idle": "IDLE",
                   "stop": "stop"})
    StateMachine.add('APPROACH_SERVICE',
                ServiceState('add_two_ints', beginner_tutorials.srv.AddTwoInts,
                    request = beginner_tutorials.srv.AddTwoIntsRequest(1,2)),
                {'succeeded':'APPROACH', 'aborted': 'APPROACH', 'preempted': 'APPROACH'})

    smach.StateMachine.add("APPROACH", Approach(),
      transitions={"done": "READY"})
  outcome = sm.execute()


if __name__ == '__main__':
    main()

