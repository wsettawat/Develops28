# import dronekit_sitl
#print ("Start simulator (SITL)")
#sitl = dronekit_sitl.start_default()
#connection_string = sitl.connection_string()
# connection_string = "/dev/ttyACM0"
# baud_rate = 115200

# Import DroneKit-Python
from dronekit import connect, VehicleMode


def init(baud_rate, port):
	# Connect to the Vehicle.
	print("Connecting to vehicle on: %s" % (port,))
	vehicle = connect(port, baud=baud_rate, wait_ready=True)
	return vehicle

def read_state(vehicle):
	return {"gps_0": str(vehicle.gps_0),
			"batt": str(vehicle.battery),
			"last_hb": str(vehicle.last_heartbeat),
			"armable": str(vehicle.armable),
			"system_status": str(vehicle.system_status.state),
			"mode": str(vehicle.mode.name)}

def read_state_fmt(vehicle):
	state = {"gps_0": vars(vehicle.gps_0),
			"batt": vars(vehicle.battery),
			"last_hb": vehicle.last_heartbeat,
			"armable": vehicle.is_armable,
			"system_status": vehicle.system_status.state,
			"mode": vehicle.mode.name}
	return {"state": state}

def read_loc(vehicle):
	return {"global_frame": str(vehicle.location.global_frame),
			"global_relative_frame": str(vehicle.location.global_relative_frame),
			"local_frame": str(vehicle.location.local_frame),
			"attitude": str(vehicle.attitude),
			"velocity": str(vehicle.velocity)}

def read_loc_fmt(vehicle):
	loc = {"glb_frame": {
				"lat": vehicle.location.global_frame.lat,
				"long": vehicle.location.global_frame.lon,
				"alt": vehicle.location.global_frame.alt 
				},
			"glb_rlt_frame": {
				"lat": vehicle.location.global_relative_frame.lat,
				"lon": vehicle.location.global_relative_frame.lon,
				"alt": vehicle.location.global_relative_frame.alt
				},
			"local_frame": {
				"north": vehicle.location.local_frame.north,
				"east" : vehicle.location.local_frame.east,
				"down" : vehicle.location.local_frame.down,
				},
			"attitude": {
				"pitch"	: vehicle.attitude.pitch,
				"yaw"	: vehicle.attitude.yaw,
				"roll"	: vehicle.attitude.roll,
				},
			"velocity": vehicle.velocity
			}
	return {"location": loc}

def read_lat_long(vehicle):
	return {"lat": vehicle.location.global_frame.lat,
			"lon": vehicle.location.global_frame.lon,
			"alt": vehicle.location.global_frame.alt,
			"pit": vehicle.attitude.pitch,
			"yaw": vehicle.attitude.yaw,
			"roll": vehicle.attitude.roll}

def read_alt(vehicle):
	return vehicle.location.global_frame.alt

def print_pixhawk(vehicle):
# Get some vehicle attributes (state) intitial
	print ("Get some intitial vehicle attribute values:")
	print (" GPS: %s" % vehicle.gps_0)
	print (" Battery: %s" % vehicle.battery)
	print (" Last Heartbeat: %s" % vehicle.last_heartbeat)
	print (" Is Armable?: %s" % vehicle.is_armable)
	print (" System status: %s" % vehicle.system_status.state)
	print (" Mode: %s" % vehicle.mode.name)    # settable

	# Printing Vehicle's Latitude
	#print("Vehicle's Latitude              =  ", vehicle.location.global_relative_frame.lat)

	# Printing Vehicle's Longitude
	#print("Vehicle's Longitude             =  ", vehicle.location.global_relative_frame.lon)
	print ("Get dynamic values:")
	print(" Global Location: %s" % vehicle.location.global_frame)
	print(" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
	print(" Local Location: %s" % vehicle.location.local_frame)
	print(" Attitude: %s" % vehicle.attitude)
	print(" Velocity: %s" % vehicle.velocity)
	# Close vehicle object before exiting script
	# vehicle.close()

def deinit(vehicle):
	vehicle.close()

# Shut down simulator
#sitl.stop()
# print("Completed")