from dronekit import connect, VehicleMode

connection_string = '127.0.0.1:14550'
# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True)


print "Basic pre-arm checks"
# Don't try to arm until autopilot is ready
while not vehicle.is_armable:
    print " Waiting for vehicle to initialise..."
    time.sleep(1)


#generate a mission for the drone
mission = generate_mission()
print "Uploading mission..."
mission.upload()
print "Uploaded!"


print "Arming motors"
vehicle.armed = True
# Confirm vehicle armed before attempting to take off
while not vehicle.armed:
    print " Waiting for arming..."
    time.sleep(1)

# Copter should arm in AUTO mode
print "Switching to AUTO mode"
vehicle.mode = VehicleMode("AUTO")
vehicle.armed = True

while True:
    nextwaypoint=vehicle.commands.next
    print 'Distance to waypoint (%s): %s' % (nextwaypoint, distance_to_current_waypoint())
    time.sleep(1)

# Close vehicle object before exiting script
vehicle.close()


def generate_mission(lat, lon, photo_alt = 2, travel_alt = 100,loiter_time = 60):
    #create a commands sequence
    cmds = vehicle.commands
    cmds.clear()

    #cmds
    takeoff = Command(0,0,0, frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                            command=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                            param1=0,
                            param2=0,
                            param3=0,
                            param4=0,
                            x=0,
                            y=0,
                            z=travel_alt)
    waypoint_high = Command(0,0,0, frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                            command=mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                            param1=0,
                            param2=0,
                            param3=0,
                            param4=0,
                            x=lat,
                            y=lon,
                            z=travel_alt)
    waypoint_low = Command(0,0,0, frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                            command=mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                            param1=0,
                            param2=0,
                            param3=0,
                            param4=0,
                            x=lat,
                            y=lon,
                            z=photo_alt)
    camera_trigger = Command(0,0,0, frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                            command = mavutil.mavlink.MAV_CMD_DO_DIGICAM_CONTROL,
                            param1=0,
                            param2=0,
                            param3=0,
                            param4=0,
                            x=0,
                            y=0,
                            z=0)
    loiter = Command(0,0,0, frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                            command = mavutil.mavlink.MAV_CMD_LOITER_TIME,
                            param1=loiter_time,
                            param2=0,
                            param3=0,
                            param4=0,
                            x=0,
                            y=0,
                            z=0)
    rtl = Command(0,0,0, frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                            command = mavutil.mavlink.MAV_CMD_RETURN_TO_LAUNCH,
                            param1=0,
                            param2=0,
                            param3=0,
                            param4=0,
                            x=0,
                            y=0,
                            z=0)

    cmds.add(takeoff)
    cmds.add(waypoint_high)
    cmds.add(waypoint_low)
    cmds.add(camera_trigger)
    cmds.add(loiter)
    cmds.add(waypoint_high)
    cmds.add(rtl)
    return cmds
