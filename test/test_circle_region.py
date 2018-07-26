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
log_vars = ['Sensor.gas']
# Where to print logging values

with IBISMotionCommander(default_height=0.5, link_uri=URI,
                         log_vars=log_vars) as mc:
    time.sleep(3)
    mc.manual_control()

    for i in range(3):
        x = mc.x
        y = mc.y
        mc.circle_region(x - 0.5, x + 0.5, y - 0.5, y + 0.5, 0.5 + 0.2*i)
        mc.stop()
        mc.move_to_point(x, y, 0.5 + 0.1*i)
        mc.stop()

    mc.print_to_file('crazyflie_data.csv')
