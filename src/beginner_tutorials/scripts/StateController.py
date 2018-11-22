import rospy 
import smach
from LoadStatemachineFromjson import LoadJson, file_config 
import types #Pathching object 
import threading
from std_msgs.msg import String
from beginner_tutorials.srv import *

curr_event_id = 0
# must provide a service for other controllers can change state of StateController
class StateController(smach.StateMachine):

    def __init__(self, datajson):

        smach.StateMachine.__init__(self, outcomes=datajson.get_outcomes())
        self.datajson = datajson 
        self.state_name = datajson.get_state()
        self.state_move = datajson.get_eventid()

        self.curr_event_id = 0 # This is changed with service called(or callback of topic) from SoundController, MovementController
        self.curr_possible_eventid = None # self.curr_event_id must in possible_eventids
        self.lock = threading.RLock() # semaphore for curr_event_id
        self.__build_statemachine()
        self.transitions_dict = dict() #dict include transitions of each state
        self.get_transitions()
        #------------- Done Contruct a State machine ----- 
        
        #------------ Build service for other controllers use -----
        #rospy.init_node("statecontroller", anonymous=True)
        rospy.Service("pusheventid", PushEventId, self.callback_push_eventid) # subscribe topic of logic controller for changing state in StateController
        print "asdasdasd"

    def __build_statemachine(self):

        self.state_object = dict() #dict consist of state object 
        self.state_outcomes = dict() # dict consists of outcomes corresponding with each state
        lock = self.lock 
        curr_event_id = self.curr_event_id #Maybe need Global variable if this way not working

        for i in self.state_name: # create state object for each state_name
            tmp_outcomes = None

            for name_state in self.state_move.keys():
                tmp_outcomes = [i["id_name"] for i in self.state_move[name_state]]
                self.state_outcomes[name_state] = tmp_outcomes
                self.state_object[name_state] = smach.State(outcomes=tmp_outcomes)
                self.state_object[name_state].name = name_state 
                self.state_object[name_state].outcomes = tmp_outcomes 
                
                #patching method for object
                def execute(self, userdata): # this self is self of State of smach
                    global curr_event_id

                    print "Hello"

                    while True:
                        for i in self.outcomes:
                            lock.acquire()
                            #print ("Executing ", self.name)
                            #print curr_event_id, self.outcomes
                            if str(curr_event_id) == i:
                                return i
                            lock.release()
                self.state_object[name_state].execute = types.MethodType(execute, self.state_object[name_state])

    # get transitions of each state from data json
    # {"id": "name_dst_state", ...}
    def get_transitions(self):
        for name_state in self.state_move.keys():
            tmp_dict = dict()
            transitions = self.state_move[name_state] # list dict move between states

            for i in transitions:
                tmp_dict[i["id_name"]] = i["dst"]
            self.transitions_dict[name_state] = tmp_dict 

    # build state controller for state machine
    def deploy(self):

        assert len(self.transitions_dict.keys()) == len(self.state_name)
        with self:
            for name_state in self.transitions_dict.keys():
                smach.StateMachine.add(name_state,self.state_object[name_state], transitions=self.transitions_dict[name_state])
        #self.execute()
        #self.register_transition_cb(f_callback)

    # ----------- Build service/topic for communicate with other controllers : SoundController, MovementController

    # push event id for change state
    # return True if can move to other state 
    # return False if cann't move to other state
    def callback_push_eventid(self, req):
        print("Event id: ", req.eventid)
        tmp = int(req.eventid)
        print("Current trainsitions  : ", self._current_transitions)
        #check this is possible 
        result = True if str(tmp) in self._current_transitions.keys() else False 
        print self._current_transitions.keys()

        if result :
            global curr_event_id 
            print("Transiting")
            self.curr_event_id = tmp 
            curr_event_id = tmp 
            return PushEventIdResponse(1)
        else:
            return PushEventIdResponse(0)


def f_callback():
     
    print ("Nothing")

if __name__ == "__main__":
    
    datajson = LoadJson(file_config)
    statecontroller = StateController(datajson)
    statecontroller.deploy()
    rospy.spin()
