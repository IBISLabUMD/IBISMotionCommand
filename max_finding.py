import logging
import time
from cflib.positioning.motion_commander import MotionCommander
from IBISMotionCommander import *
import cflib.crtp
from manual_control import *

URI = 'radio://0/80/250K'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# Initialize the low-level drivers (don't list the debug drivers)
cflib.crtp.init_drivers(enable_debug_driver=False)
# The values that indicate where the crazyflie thinks it is
log_vars = [ 'kalman.stateX', 'kalman.stateY', 'kalman.stateZ']
# Where to print logging values
log_file = 'crazyflie_data.csv'
square_spiral = False

with IBISMotionCommander(link_uri=URI, log_file=log_file, log_vars=log_vars) as mc:
    time.sleep(3)
    mc.manual_control()
    mc.spiral_in()
    mc.spiral_out()
    entries = mc.entries()
    max_gas_index = 0
    for i, entry in enumerate(entries):
       if entry['Sensor.gas'] > entries[max_gas_index]['Sensor.gas']:
           max_gas_index = i
    max_gas_entry = entries[max_gas_index]
    curr_x = mc['kalman.stateX']
    curr_y = mc['kalman.stateY']
    curr_z = mc['kalman.stateZ']
    new_x = max_gas_entry['kalman.stateX']
    new_y = max_gas_entry['kalman.stateY']
    new_z = max_gas_entry['kalman.stateZ']
    mc.move_distance(new_x - curr_x, new_y - curr_y, new_z - curr_z + 0.2)
    mc.stop()
    time.sleep(5)




   

