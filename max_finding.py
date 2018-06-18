import logging
import time
from cflib.positioning.motion_commander import MotionCommander
from IBISMotionCommander import *
import cflib.crtp

URI = 'radio://0/80/250K'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# Initialize the low-level drivers (don't list the debug drivers)
cflib.crtp.init_drivers(enable_debug_driver=False)
# The values that indicate where the crazyflie thinks it is
log_vars = ['Sensor.gas', 'controller.yaw', 'kalman.stateX', 'kalman.stateY', 'kalman.stateZ']
# Where to print logging values
log_file = 'crazyflie_data.csv'
square_spiral = False

with IBISMotionCommander(default_height=0.5, link_uri=URI, log_file=log_file, log_vars=log_vars) as mc:
    time.sleep(3)
    mc.manual_control()
    start_index = len(mc.entries())
    for level in range(1, 4, 1): 
        print('spiraling')
        spacing = 0.25 - (level - 1) * 0.05
        velocity = 0.2 - (level - 1) *0.05
        max_radius = 1.5 / level
        mc.spiral_out(max_radius=max_radius, spacing=spacing, velocity=velocity)
        print('stopping')
        mc.stop()
        print('calculating')
        entries = mc.entries()[start_index:]
        max_gas_index = 0 
        for i, entry in enumerate(entries):
           if entries[i]['Sensor.gas'] > entries[max_gas_index]['Sensor.gas']:
               max_gas_index = i
        max_gas_entry = entries[max_gas_index]
        new_x = max_gas_entry['kalman.stateX']
        new_y = max_gas_entry['kalman.stateY']
        new_z = max_gas_entry['kalman.stateZ']
        if new_z < 0.5:
            print('height error')
            print('z distance is: ' + str(new_z))
            new_z = 0.5
        mc.stop()
        print('turning crazyflie to 0 degrees yaw')
        mc.turn_to_zero()
        print('moving crazyflie')
        curr_x = mc['kalman.stateX']
        curr_y = mc['kalman.stateY']
        curr_z = mc['kalman.stateZ']
        mc.move_distance(new_x - curr_x, new_y - curr_y, new_z - curr_z)
        print('stopping')
        mc.stop()
        print('going up')
        mc.up(0.2)
        print('stopping')
        mc.stop()
        start_index = len(mc.entries())
