from dronekit import connect, VehicleMode, Command
import time
from pymavlink import mavutil
import math



class DroneDispatch():

    def __init__(self,vehicle,travel_alt = 100):
        self.vehicle = vehicle
        self.travel_alt = travel_alt

    def dispatch(self, lat, lon, alt):

        print "Basic pre-arm checks"
        # Don't try to arm until autopilot is ready
        while not self.vehicle.is_armable:
            print " Waiting for self.vehicle to initialise..."
            time.sleep(1)

        self.vehicle.mode = VehicleMode("GUIDED")

        #generate a mission for the drone
        mission = self.generate_mission(lat,lon,photo_alt = alt)
        print "Uploading mission..."
        mission.upload()
        print "Uploaded!"


        print "Arming motors"
        self.vehicle.armed = True
        # Confirm self.vehicle armed before attempting to take off
        while not self.vehicle.armed:
            print " Waiting for arming..."
            time.sleep(1)

        # Copter should arm in AUTO mode
        print "Switching to AUTO mode"
        self.vehicle.mode = VehicleMode("AUTO")

        print "Taking off"
        msg = self.vehicle.message_factory.command_long_encode(
                0, 0,    # target system, target component
                mavutil.mavlink.MAV_CMD_MISSION_START, #command
                0,0,0,0,0,0,0,0)
        self.vehicle.send_mavlink(msg)


    def generate_mission(self, lat, lon, photo_alt = 2, loiter_time = 60):
        #create a commands sequence
        cmds = self.vehicle.commands
        cmds.clear()

        #cmds
        takeoff = Command(0,0,0,current=0, autocontinue=0,
                                frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                command=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                param1=0,
                                param2=0,
                                param3=0,
                                param4=0,
                                x=0,
                                y=0,
                                z=self.travel_alt)
        waypoint_high = Command(0,0,0,current=0, autocontinue=0,
                                frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                command=mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                                param1=0,
                                param2=0,
                                param3=0,
                                param4=0,
                                x=lat,
                                y=lon,
                                z=self.travel_alt)
        waypoint_low = Command(0,0,0,current=0, autocontinue=0,
                                frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                command=mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                                param1=0,
                                param2=0,
                                param3=0,
                                param4=0,
                                x=lat,
                                y=lon,
                                z=photo_alt)
        camera_trigger = Command(0,0,0,current=0, autocontinue=0,
                                frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                command = mavutil.mavlink.MAV_CMD_DO_DIGICAM_CONTROL,
                                param1=0,
                                param2=0,
                                param3=0,
                                param4=0,
                                x=0,
                                y=0,
                                z=0)
        loiter = Command(0,0,0,current=0, autocontinue=0,
                                frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                command = mavutil.mavlink.MAV_CMD_NAV_LOITER_TIME,
                                param1=loiter_time,
                                param2=0,
                                param3=0,
                                param4=0,
                                x=0,
                                y=0,
                                z=0)
        rtl = Command(0,0,0,current=0, autocontinue=0,
                                frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                command = mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
                                param1=0,
                                param2=0,
                                param3=0,
                                param4=0,
                                x=0,
                                y=0,
                                z=0)

        cmds.add(takeoff)
        cmds.add(takeoff)
        cmds.add(waypoint_high)
        cmds.add(waypoint_low)
        cmds.add(camera_trigger)
        cmds.add(loiter)
        cmds.add(waypoint_high)
        cmds.add(rtl)
        return cmds


if __name__ == "__main__":
    # Connect to the Vehicle.
    print("Connecting to vehicle")
    vehicle = connect("127.0.0.1:14550", wait_ready=['armed','mode'])

    dd = DroneDispatch(vehicle,15)
    dd.dispatch(-35.362128, 149.165072,5)
    time.sleep(2)
    vehicle.close()
