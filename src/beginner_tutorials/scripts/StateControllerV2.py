#!/usr/bin/env python
import rospy 
import smach
from LogicControllerV2 import LogicControllerV2 
import Queue

class IDLE(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=["to_active", "none"])

  def execute(self, userdata):
    rospy.loginfo("Executing state IDLE")
    return "to_active"


class Activation(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=["to_ready", "stop"])

  def execute(self, userdata):
    rospy.loginfo("Executing state Hey")
    return "to_ready"


class Ready(smach.State):
  def __init__(self):
    smach.State.__init__(self, outcomes=["to_activation"])

  def execute(self, userdata):
    rospy.loginfo("Executing state Ready")
    return "to_activation"

class StateControllerV2(object):
    def __init__(self):
      rospy.init_node("appControllerv2")
      self.event_queues = Queue.Queue()
      LogicControllerV2(self)
    
    def execute(self):   
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
      outcome = sm.execute()


    def pushToEventQueues(self, event_id):
        self.event_queues.put(event_id)
    
if __name__ == "__main__":
  
  statecontroller = StateControllerV2()
  print("---------")
  rospy.spin()
