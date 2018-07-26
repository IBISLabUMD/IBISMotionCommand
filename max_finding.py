# from math import cos, sin, pi
import logging
import time
from IBISMotionCommander import IBISMotionCommander
import cflib.crtp

URI = 'radio://0/80/250K'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# Initialize the low-level drivers (don't list the debug drivers)
cflib.crtp.init_drivers(enable_debug_driver=False)
# The values that indicate where the crazyflie thinks it is
log_vars = ['Sensor.gas', 'controller.yaw',
            'kalman.stateX', 'kalman.stateY', 'kalman.stateZ']
# Where to print logging values
log_file = 'crazyflie_data.csv'

with IBISMotionCommander(default_height=0.5, link_uri=URI,
                         log_file=log_file, log_vars=log_vars) as mc:
    time.sleep(3)
    mc.manual_control()
    z = 0.5
    start = len(mc.data)
    for level in range(1, 4):
        max_radius = 1.5 - (level - 1) * 0.5
        print('spiraling')
        spacing = 0.25 - (level - 1) * 0.05
        velocity = 0.25 - (level - 1) * 0.05
        # print(f'new max_radius is: {max_radius}')
        mc.spiral_out(max_radius=max_radius,
                      spacing=spacing, velocity=velocity)
        print('stopping')
        mc.stop()
        print('calculating')
        stop = len(mc.data)
        print(f'start: {start}\nstop: {stop}')
        xmin, xmax, ymin, ymax = mc.gas_region(start=start, stop=stop,
                                               threshhold=0.7)
        start = len(mc.data)
        mc.circle_region(xmin, xmax, ymin, ymax, z)

#        max_radius = 1.0 * max([xmax - xmin, ymax - ymin]) / 2
        x = (xmax + xmin) / 2
        y = (ymax + ymin) / 2
        z += 0.2
        mc.stop()
        mc.turn_to_point(x, y)
        print('moving crazyflie')
        mc.move_to_point(x, y, z)
        print('stopping')
        mc.stop()
