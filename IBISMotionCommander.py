from math import cos, sin, pi, atan2, degrees, sqrt
import time
from cflib.positioning.motion_commander import MotionCommander


def normalize_yaw(yaw):
    yaw %= 360
    return yaw if yaw < 180 else yaw - 360


class IBISMotionCommander(MotionCommander):
    MotionCommander.VELOCITY += 0.2
    MotionCommander.RATE += 72

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
        yaw = self.yaw
        while abs(self.yaw) > 0.5:
            if yaw > 0:
                self.turn_right(yaw)
            else:
                self.turn_left(-yaw)
            yaw = self.yaw

    def calculate_inertial_xy(self, x, y):
        yaw = self.yaw
        cos_yaw = cos(yaw * pi / 180)
        sin_yaw = sin(yaw * pi / 180)
        inertial_x = x * cos_yaw + y * sin_yaw
        inertial_y = - x * sin_yaw + y * cos_yaw
        return inertial_x, inertial_y

    def velocity_vector(self, x, y, z):
        diff_x, diff_y = self.calculate_inertial_xy(x - self.x, y - self.y)
        diff_z = z - self.z
        distance = sqrt(diff_x**2 + diff_y**2 + diff_z**2)
        vel_x = diff_x / distance * MotionCommander.VELOCITY
        vel_y = diff_y / distance * MotionCommander.VELOCITY
        vel_z = diff_z / distance * MotionCommander.VELOCITY
        return (vel_x, vel_y, vel_z)

    def move_to_point(self, x, y, z):
        while self.distance(x, y, z) > 0.05:
            velocities = self.velocity_vector(x, y, z)
            self.start_linear_motion(*velocities)
            time.sleep(0.1)

    def new_yaw(self, x, y):
        return degrees(atan2(y - self.y, x - self.x))

    def turn_to_point(self, x, y):
        yaw_diff = normalize_yaw(self.yaw - self.new_yaw(x, y))
        while abs(yaw_diff) > 1:
            if yaw_diff > 0:
                self.turn_right(yaw_diff)
            else:
                self.turn_left(-yaw_diff)
            yaw_diff = normalize_yaw(self.yaw - self.new_yaw(x, y))
            print(f'yaw diff is: {yaw_diff}')

    def distance(self, x, y, z):
        return sqrt((self.x - x)**2 + (self.y - y)**2 + (self.z - z)**2)

    def distance2d(self, x, y):
        return sqrt((self.x - x)**2 + (self.y - y)**2)

    def gas_region(self, start=0, stop=-1, threshhold=0.9):
        gases = self.data['Sensor.gas'][start:stop]
        xs = self.xs[start:stop]
        ys = self.ys[start:stop]
        zs = self.zs[start:stop]

        min_gas = min(gases)
        max_gas = max(gases)
        max_gas_index = gases.index(max_gas)
        gas_threshhold = min_gas + threshhold * (max_gas - min_gas)

        xmin = xs[max_gas_index]
        ymin = ys[max_gas_index]
        xmax = xmin
        ymax = ymin
        for gas, x, y, z in zip(gases, xs, ys, zs):
            if gas > gas_threshhold:
                if x < xmin:
                    xmin = x
                elif x > xmax:
                    xmax = x
                if y < ymin:
                    ymin = y
                elif y > ymax:
                    ymax = y
        return (xmin, xmax, ymin, ymax)

    def route(self, xmin, xmax, ymin, ymax):
        corners = [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)]
        distance_to_corners = [self.distance2d(*corner) for corner in corners]
        start_index = distance_to_corners.index(min(distance_to_corners))
        return corners[start_index:] + corners[:start_index]

    def circle_region(self, xmin, xmax, ymin, ymax, z):
        for corner in self.route(xmin, xmax, ymin, ymax):
            self.turn_to_point(corner)
            print(corner)
            self.move_to_point(*corner, z)
            self.stop()

#    def plot(self):
#        import matplotlib.pyplot as plt
#        import matplotlib.animation as animation
#
#        fig = plt.figure()
#        ax = fig.Axes3D(fig)
#        line, = ax.plot3D(self.xs, self.ys, self.zs, color='k')
#
#        def update(args*):
#            fig.axes.axis([-2, 2, -2, 2, 0, 2])
#            ax.plot3D(self.xs, self.ys, self.zs, color='k')
#            return line,
#
#        ani = animation.FuncAnimation(fig, update, None,
#                                      interval=10, blit=True, repeat=False)
