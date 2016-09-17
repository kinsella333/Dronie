from printer import Printer
from camera import Camera


connection_string = '127.0.0.1:14550'
TRIGGER_WP = 5

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=['armed','mode'])

#open raspi camera
camera = Camera()

#connect to polaroid printer
printer = Printer()

while True:
    #Wait for the drone to be in proper mode
    while not vehicle.armed or vehicle.mode.name != "AUTO":
        print "Waiting for drone to enter AUTO mode"
        time.sleep(1)

    #start recording our mission
    camera.start()

    #wait for drone to arrive a trigger waypoint
    last_print = 0
    while vehicle.commands.next != TRIGGER_WP:
        if last_print != vehicle.commands.next:
            print "Going to WP: {}".format(vehicle.commands.next)
        time.sleep(0.1)
    print "Arrived at client!"

    #take picture
    print "Taking picture"
    file_path = camera.capture()

    #print picture
    if debug:
        print "WARNING: PRINTING PICTURE IN DEBUG MODE"
    else:
        successful_print = printer.send_to_printer(file_path)
        if successful_print:
            print "Print sent successfully!"


    #wait for disarm before processing next client
    while vehicle.armed:
        print "Waiting for vehicle to disarm before processing next client"

    camera.stop()
    time.sleep(2)
