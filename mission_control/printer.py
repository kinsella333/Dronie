import time
import subprocess
import os

'''
#check save location
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
#save file
filename = save_dir + post.id + ".jpg"
img.save(filename, 'JPEG')
#print file
if debug:
    img.show()
else:
    successful_print = send_to_printer(filename)
'''



class Printer():

    def __init__(self):
        #config variables
        self.printer_MAC = "00:04:48:10:7E:36"
        self.save_dir = "/home/pi/pics/"

    #sys_call - make a blocking system call
    def sys_call(self, cmd):
        p = subprocess.Popen([cmd], stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()[0]
        return out

    # send_to_printer - transfer a file to the bluetooth printer
    def send_to_printer(self, sourcefile):
        try:
            #connecting to printer
            self.sys_call("rfkill unblock bluetooth")
            self.sys_call("rfcomm unbind /dev/rfcomm0 " + self.printer_MAC)
            self.sys_call("rfcomm bind /dev/rfcomm0 " + self.printer_MAC)
            #print image
            out = self.sys_call("ussp-push /dev/rfcomm0 " + sourcefile + " destfile.jpg")
            if out.find("Error") == 0:
                 print("[ Error ] Unable to transfer file to printer")
                 return False
        except OSError:
            print("[ Error ] Unable to execute bluetooth print")
            return False

        return True
