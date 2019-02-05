# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2017 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
This script shows the basic use of the MotionCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. This script requires some kind of location system, it has been
tested with (and designed for) the flow deck.

Change the URI variable to your Crazyflie configuration.
"""
# from math import cos, sin, pi
import logging
import time
from IBISMotionCommander import IBISMotionCommander
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie import Crazyflie
from CrazymothLogger import *
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
log_file = 'pinpoint_data_0602.list'

def wait_for_position_estimator(scf):
    print('Waiting for estimator to find position...')

    log_config = LogConfig(name='Kalman Variance', period_in_ms=500)
    log_config.add_variable('kalman.varPX', 'float')
    log_config.add_variable('kalman.varPY', 'float')
    log_config.add_variable('kalman.varPZ', 'float')

    var_y_history = [1000] * 10
    var_x_history = [1000] * 10
    var_z_history = [1000] * 10

    threshold = 0.001

    with SyncLogger(scf, log_config) as logger:
        for log_entry in logger:
            data = log_entry[1]

            var_x_history.append(data['kalman.varPX'])
            var_x_history.pop(0)
            var_y_history.append(data['kalman.varPY'])
            var_y_history.pop(0)
            var_z_history.append(data['kalman.varPZ'])
            var_z_history.pop(0)

            min_x = min(var_x_history)
            max_x = max(var_x_history)
            min_y = min(var_y_history)
            max_y = max(var_y_history)
            min_z = min(var_z_history)
            max_z = max(var_z_history)

            # print("{} {} {}".
            #       format(max_x - min_x, max_y - min_y, max_z - min_z))

            if (max_x - min_x) < threshold and (
                    max_y - min_y) < threshold and (
                    max_z - min_z) < threshold:
                break


with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
    # We take off when the commander is created
    arr = None
    with CrazyLogger(log_file_name=log_file,
                    scf=scf,
                    log_vars=log_vars) as cl:
        with IBISMotionCommander(scf, default_height=0.3) as mc: 

            time.sleep(3)
            mc.manual_control()
            z = 0.3
            direction = "left"
            for level in range(1,4):
                if level == 1:
                    print("---------------------------level 1----------------------------------------------------------------")
                    max_radius = 1.5
                    spacing = 0.3 - (level - 1) * 0.5
                    velocity = 0.25 - (level - 1) * 0.5

                    cl.clear_gas()
                    print("spiraling level 1.....") 
                    mc.spiral_out(max_radius=max_radius, spacing=spacing, direction=direction, velocity=velocity)
                    print("stopping.....")
                    mc.stop()
                    print("calculating.....")

                    logvalues = cl.gas_data()
                    gases_val = mc.get_gas(logvalues)
                    x_int = mc.get_gas_x(logvalues)
                    y_int = mc.get_gas_y(logvalues)
                    z_int = mc.get_gas_z(logvalues)

                    print("gases val: ", gases_val)
                    print("x_int: ", x_int)
                    print("y_int: ", y_int)
                    print("z_int: ", z_int)

                    x, y, radius = mc.gas_radius(gases=gases_val, xs=x_int, ys=y_int, zs=z_int, log_values=logvalues, threshold=0.7)
                    z = 0.5

                    print("----------------level 1 into 2 x and y location-------------------------------")
                    print("x:", x)
                    print("y:", y)
                    print("radius:", radius)
                    print("------------------------------------------------------------------------------")

                elif level == 2:
                    print("--------------------------level 2--------------------------------------------------------------------")
                    max_radius = 0.9
                    spacing = (max_radius * 0.4) / 1.5
                    velocity = 0.2
                    cl.clear_gas()
                    
                    time.sleep(3)
                    print("moving to center for level 2.....")
                    current_position = cl.current_position()
                    current_x = current_position.get('kalman.stateX')
                    current_y = current_position.get('kalman.stateY')
                    current_z = current_position.get('kalman.stateZ')
                    current_yaw = current_position.get('controller.yaw')

                    print("current_x:", current_x)
                    print("current_y:", current_y)
                    print("current_z:", current_z)
                    print("current_yaw:", current_yaw)

                    mc.turn_to_point(x, y, current_position)
                    mc.move_to_point(x, y, z, current_position)
                    print("spiraling level 2.....")
                    mc.spiral_out(max_radius=max_radius, spacing=spacing, direction=direction, velocity=velocity)
                    print("stopping.....")
                    mc.stop()
                    print("calculating.....")

                    logvalues = cl.gas_data()
                    gases_val = mc.get_gas(logvalues)
                    x_int = mc.get_gas_x(logvalues)
                    y_int = mc.get_gas_y(logvalues)
                    z_int = mc.get_gas_z(logvalues)

                    print("gases val: ", gases_val)
                    print("x_int: ", x_int)
                    print("y_int: ", y_int)
                    print("z_int: ", z_int)

                    x, y, radius = mc.gas_radius(gases=gases_val, xs=x_int, ys=y_int, zs=z_int, log_values=logvalues, threshold=0.7)
                    z = 0.6
                    
                    print("----------------level 2 into 3 x and y location-------------------------------")
                    print("x:", x)
                    print("y:", y)
                    print("radius:", radius)
                    print("------------------------------------------------------------------------------")
                
                elif level == 3:
                    print("-------------------------------level 3------------------------------------------------------------------")
                    max_radius = 0.7
                    spacing = (max_radius * 0.4) / 1.5
                    velocity = 0.15
                    cl.clear_gas()

                    time.sleep(3)
                    print("moving to center for level 3.....")
                    current_position = cl.current_position()
                    mc.turn_to_point(x, y, current_position)
                    mc.move_to_point(x, y, z, current_position)
                    mc.spiral_out(max_radius=max_radius, spacing=spacing, direction=direction, velocity=velocity)
                    print("stopping.....")
                    mc.stop()
                    print("calculating.....")

                    logvalues = cl.gas_data()
                    gases_val = mc.get_gas(logvalues)
                    x_int = mc.get_gas_x(logvalues)
                    y_int = mc.get_gas_y(logvalues)
                    z_int = mc.get_gas_z(logvalues)

                    x, y, radius = mc.gas_radius(gases=gases_val, xs=x_int, ys=y_int, zs=z_int, log_values=logvalues, threshold=0.7)

                    print("-----------------------------------------------")
                    print("level at 3 x and y location")
                    print("x:",x)
                    print("y:",y)
                    print("radius:", radius)
                    print("-----------------------------------------------")

                    print("pinpointing peanut.....")
                    time.sleep(3)
                    current_position = cl.current_position()
                    mc.turn_to_point(x, y, current_position)
                    mc.move_to_point(x, y, z, current_position)
                    time.sleep(5)
                    print("gas source estimated location...")
                    mc.stop()
                    print("landing......")
                    mc.land(velocity=0.1)
            
            
