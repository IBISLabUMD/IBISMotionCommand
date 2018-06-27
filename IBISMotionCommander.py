from math import cos, sin, pi
import time
from cflib.positioning.motion_commander import MotionCommander


class IBISMotionCommander(MotionCommander):

    def __init__(self, *args, **kwargs):
        MotionCommander.__init__(self, *args, **kwargs)

    def manual_control(self, distance=0.15, velocity=0.5):
        ctrl_token = ''
        print('a = left, d = right, w = forward, s = back')
        print('1 = turn left, 2 = turn right, k = up, j = down, q = quit')
        while ctrl_token != 'q':
            time.sleep(0.1)
            ctrl_token = input('Provide Control Token:')
            if ctrl_token == 'a':
                self.left(distance, velocity)
            elif ctrl_token == 'd':
                self.right(distance, velocity)
            elif ctrl_token == 'w':
                self.forward(distance, velocity)
            elif ctrl_token == 's':
                self.back(distance, velocity)
            elif ctrl_token == '1':
                self.turn_left(20, 20)
            elif ctrl_token == '2':
                self.turn_right(20, 20)
            elif ctrl_token == 'k':
                self.up(distance, velocity)
            elif ctrl_token == 'j':
                self.down(distance, velocity)
            else:
                self.stop()

    def spiral_in(self, max_radius=1, spacing=0.15, direction='left'):
        radius = max_radius
        while radius > spacing:
            if direction == 'left':
                self.circle_left(radius, angle_degrees=180)
            else:
                self.circle_right(radius, angle_degrees=180)
            radius -= spacing

    def spiral_out(self, max_radius=1, spacing=0.15, direction='left',
                   velocity=0.2):
        radius = spacing
        while radius < max_radius:
            if direction == 'left':
                self.circle_left(radius, angle_degrees=180, velocity=velocity)
            else:
                self.circle_right(radius, angle_degrees=180)
            radius += spacing

    def square_spiral_out(self, max_radius=1, spacing=0.15, direction='left'):
        radius = spacing
        while radius < max_radius:
            self.forward(radius)
            self.turn_left(90, 45)
            self.forward(radius)
            self.turn_left(90, 45)
            radius += spacing

    def turn_to_zero(self):
        yaw = self['controller.yaw']
        while abs(yaw) > 1:
            if yaw > 0:
                self.turn_right(yaw)
            else:
                self.turn_left(yaw)
            yaw = self['controller.yaw']

    def calculate_inertial_xy(self, x, y):
        yaw = self['controller.yaw']
        cos_yaw = cos(yaw * pi / 180)
        sin_yaw = sin(yaw * pi / 180)
        inertial_x = x * cos_yaw + y * sin_yaw
        inertial_y = - x * sin_yaw + y * cos_yaw
        return inertial_x, inertial_y

    def move_to_point(self, x, y, z):
        diff_x, diff_y = self.calculate_inertial_xy(x - self['kalman.stateX'],
                                                    y - self['kalman.stateY'])
        diff_z = z - self['kalman.stateZ']
        distance = (diff_x**2 + diff_y**2 + diff_z**2)**0.5
        while distance > 0.05:
            self.move_distance(diff_x, diff_y, diff_z)
            diff_x, diff_y = self.calculate_inertial_xy(
                                                    x - self['kalman.stateX'],
                                                    y - self['kalman.stateY'])
            diff_z = z - self['kalman.stateZ']
            distance = (diff_x**2 + diff_y**2 + diff_z**2)**0.5

    def run_sequence(self, sequence):
        cf = self.cf

        cf.param.set_value('flightmode.posSet', '1')

        for position in sequence:
            print('Setting position {}'.format(position))
            for i in range(50):
                cf.commander.send_setpoint(position[1], position[0],
                                           position[3],
                                           int(position[2] * 1000))
                time.sleep(0.1)

        #cf.commander.send_setpoint(0, 0, 0, 0)
        # Make sure that the last packet leaves before the link is closed
        # since the message queue is not flushed before closing
        time.sleep(0.1)
