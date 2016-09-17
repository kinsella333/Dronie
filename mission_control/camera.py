import time
from dronekit import connect
import picamera
import os.path
import time


class Camera():

    def __init__(self):
        self.camera = picamera.PiCamera()

    def start(self):
        #enumerate file path
        base_path = "/home/pi/vids/dronie"
        i = 0
        while os.path.exists(base_path + str(i) + ".h264"):
            i+=1
        file_path = base_path + str(i) + ".h264"

        #start recording
        print "Recording to {}".format(file_path)
        self.camera.start_recording(file_path)

    def stop(self):
        print "Stopped recording"
        self.camera.stop_recording()

    def capture(self):
        base_path = "/home/pi/pics/dronie"
        i = 0
        while os.path.exists(base_path + str(i) + ".jpg"):
            i+=1
        #capture still
        file_path = base_path + str(i) + ".jpg"

        print "Captured {}".format(file_path)
        self.camera.capture(file_path,use_video_port=True)
        return file_path
