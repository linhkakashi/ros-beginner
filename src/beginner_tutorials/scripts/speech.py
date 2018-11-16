#!/usr/bin/env python
import speech_recognition as sr
import rospy
from robotics.msg import SoundRecog 
from robotics.srv import SoundLocation
import robotics

def voice_recog():
    pub = rospy.Publisher('voice_recog', SoundRecog, queue_size=100)
    get_SL = rospy.ServiceProxy('sound_localization', SoundLocation)
    req = robotics.srv.SoundLocationRequest(0)

    rospy.init_node('voice_recog_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    print("Say something!")
    while not rospy.is_shutdown():
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:	
            audio = r.listen(source)
            print("Listening")
            
            resp = get_SL(req)
            print ("got: ")
            print(resp)
            try:
                SoundRecogFrame = SoundRecog()
		SoundRecogFrame.header.stamp = rospy.get_rostime()
                SoundRecogFrame.data = r.recognize_google(audio)
                SoundRecogFrame.angle = resp.angle
                print(SoundRecogFrame.data)
                pub.publish(SoundRecogFrame)
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

if __name__ == '__main__':
    voice_recog()

