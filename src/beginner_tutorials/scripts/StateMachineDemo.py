#!/usr/bin/env python

import rospy
import smach
from std_msgs.msg import String 

control_var = 0

def call_back_change_control_var(data):

    global control_var
    tmp = data.data
    print "asdasd", data.data, control_var
    print str(tmp)=="hey"
    #exit()
    if tmp == "hey":
        global control_var
        control_var = 3

# define state Foo
class Foo(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        while 1:

            if control_var == 0:
                return 'outcome1'
            if control_var == 3:
                return 'outcome2'

            #rospy.spin()


# define state Bar
class Bar(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome2'])

    def execute(self, userdata):
        rospy.loginfo('Executing state BAR')
        return 'outcome2'
        


class ControllerState(smach.StateMachine):

    def __init__(self):

        smach.StateMachine.__init__(self, outcomes=['outcome4', 'outcome5'])
        with self:
	    smach.StateMachine.add('FOO', Foo(),
                       transitions={'outcome1':'BAR',
                                    'outcome2':'outcome4'})
	    smach.StateMachine.add('BAR', Bar(),
                       transitions={'outcome2':'FOO'})


    #def execute(self, userdata):
    #    while 1:

# main
def main():
    rospy.init_node('smach_example_state_machine')
    rospy.Subscriber("chatter", String, call_back_change_control_var)
    #rospy.spin()
    # Create a SMACH state machine
    #sm = smach.StateMachine(outcomes=['outcome4', 'outcome5'])
    sm = ControllerState()

    # Execute SMACH plan
    outcome = sm.execute()
    rospy.spin()


if __name__ == '__main__':
    main()
