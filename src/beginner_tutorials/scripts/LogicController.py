import rospy
from beginner_tutorials.srv import *

class LogicController(object):

    def __init__(self):
        
        #rospy.init_node("logiccontroller", anonymous=True)
        self.pub = rospy.Service("pusheventid_tologic", PushEventId, self.callback_push_eventid)

        #follow service of StateController
        self.push_event_id = None 
        self.push_success = True 

        try:
            self.push_event_id = rospy.ServiceProxy("pusheventid", PushEventId)
        except rospy.ServiceException, e:
            print("Service call fail, ", e)
            self.push_success = False 
        
        self.get_sound_data = None 
        try:
            self.get_sound_data = rospy.ServiceProxy("pushsounddata", DataSound)
        except rospy.ServiceException, e:
            print("Service call fail, ", e)

    # process data of other controller
    def process_sound_data(self):
        
        tmp = False 

        if self.get_sound_data is not None:
            data_sound = self.get_sound_data("")
            print "data_sound : " , data_sound

            if data_sound.data == "hey":
                print "Calling service statecontroller from logic controller"
                tmp = self.push_event_id_to_statecontroller(3)
        return tmp 

    def push_event_id_to_statecontroller(self, i):

        assert self.push_event_id is not None 

        try:    
            self.push_success = self.push_event_id(i)
        except rospy.ServiceException, e:
            print("Call service fail: ", e)


    def callback_push_eventid(self, req):
        
        print "Service push id to StateController calling"
        print("Event id: ", req.eventid)
        tmp = int(req.eventid)
        #print(self._current_transitions)
        #check this is possible 
        result = self.process_sound_data()

        if result :
            #self.curr_event_id = tmp
            return PushEventIdResponse(1)
        else:
            return PushEventIdResponse(0)

