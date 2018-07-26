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

with IBISMotionCommander(default_height=0.5, link_uri=URI) as mc:

    time.sleep(3)

    mc.manual_control()

    group = 'pid_rate'
    name = 'yaw_ki'
    full_name = group + '.' + name

    yaw_ki = mc.param.toc.get_element(group, name)
    print(yaw_ki)  # should be 16.7

    yaw_ki -= 1
    mc.param.set_value(full_name, yaw_ki)
    time.sleep(3) # adjust in case value doesn't update
    yaw_ki = mc.param.toc.get_element(group, name)
    print(yaw_ki)  # should be 15.7

    yaw_ki += 1 
    mc.param.set_value(full_name, yaw_ki)
    time.sleep(3) # adjust in case value doesn't update
    yaw_ki = mc.param.toc.get_element(group, name)
    print(yaw_ki)  # should be 16.7
