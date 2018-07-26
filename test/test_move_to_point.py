import logging
import time
from IBISMotionCommander import IBISMotionCommander
import cflib.crtp

URI = 'radio://0/80/250K'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# Initialize the low-level drivers (don't list the debug drivers)
cflib.crtp.init_drivers(enable_debug_driver=False)

with IBISMotionCommander(default_height=0.5, link_uri=URI) as mc:

    time.sleep(3)
    mc.move_to_point(0.5, 0.5, 0.5)
    print('the crazyflie thinks its at point')
    print(mc.data[-1])
    time.sleep(1)
    for _ in range(3):
        mc.turn_to_point(0.5, 0.5+1)
        mc.move_to_point(0.5, 0.5+1, 0.5)
        mc.turn_to_point(0.5-1, 0.5)
        mc.move_to_point(0.5-1, 0.5, 0.5)
        mc.turn_to_point(0.5, 0.5-1)
        mc.move_to_point(0.5, 0.5-1, 0.5)
        mc.turn_to_point(0.5+1, 0.5)
        mc.move_to_point(0.5+1, 0.5, 0.5)
