import rospy
from StateController import StateController 
from LogicController import LogicController 
from LoadStatemachineFromjson import LoadJson, file_config 

class AppController(object):

    def __init__(self):
        rospy.init_node("appcontroller", anonymous=True)
        self.datajson = LoadJson(file_config)
        self.statecontroller = StateController(self.datajson)
        print("23543453")
        self.statecontroller.deploy()
        print "Set up statecontroller done!!"

        self.logiccontroller = LogicController()
        self.statecontroller.execute()

    def execute(self):
        pass 

if __name__ == "__main__":
    
    appcontroller = AppController()
    print ("---------")
    rospy.spin()

