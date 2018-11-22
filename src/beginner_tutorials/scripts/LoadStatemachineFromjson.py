import rospy 
import smach 
import json 

file_config = "config.json"

# get state and connect between states
class LoadJson(object):

    def __init__(self, file_config):

        self.file_config = file_config 
        statemachine_infor = json.load(open(self.file_config, 'r'))
        assert "state" in statemachine_infor.keys() and "event_id" in statemachine_infor.keys() and "end_state" in statemachine_infor.keys()

        self.state = statemachine_infor["state"]
        self.event_id = statemachine_infor["event_id"]
        self.end_state = statemachine_infor["end_state"]

        #print self.state 
        #print self.event_id
        #print self.end_state
    
    def get_state(self):
        return self.state 

    def get_eventid(self):
        return self.event_id 

    def get_outcomes(self):
        return self.end_state
    
    # functions check comfortable json file 

    def check_unique_eventid(self):
        pass 

if __name__ == "__main__":

    loadjson = LoadJson(file_config)
        
