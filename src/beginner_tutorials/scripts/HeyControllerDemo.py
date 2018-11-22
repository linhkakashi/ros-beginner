import rospy 
from std_msgs.msg import String 
from beginner_tutorials.srv import *

class SoundController(object):

    def __init__(self):
        rospy.init_node("soundcontroller", anonymous=True)
        rospy.wait_for_service("pusheventid_tologic")
        
        self.push_success = True 
        try:
            self.push_event_id = rospy.ServiceProxy("pusheventid_tologic", PushEventId)
            print self.push_event_id
        except rospy.ServiceException, e:
            print("Call service fail: ", e)
            self.push_success = False

        # create service push data
        self.sub = rospy.Service("pushsounddata", DataSound, self.push_handle_sound)

    def push_event_id_to_logic(self, i):

        try:
            self.push_success = self.push_event_id(i)
        except rospy.ServiceException, e:
            print("Call service faillll: ", e)

    def push_handle_sound(self, req):

        a = raw_input("Speech: ")
        return DataSoundResponse(a)

if __name__ == "__main__":
    print ("Hello")
    soundcontroller = None
    try:
        soundcontroller = SoundController()
    except rospy.ROSInterruptException:
        pass
    
    soundcontroller.push_event_id_to_logic(3)
