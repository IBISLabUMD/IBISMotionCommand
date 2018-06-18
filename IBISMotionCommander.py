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

    def spiral_in(self, max_radius=1, spacing=0.1, direction='left'):
        radius = max_radius
        while radius > spacing:
            if direction == 'left':
                self.circle_left(radius, angle_degrees=180)
            else:
                self.circle_right(radius, angle_degrees=180)
            radius -= spacing 

    def spiral_out(self, max_radius=1, spacing=0.1, direction='left'):
        radius = spacing
        while radius < max_radius:
            if direction == 'left':
                self.circle_left(radius, angle_degrees=180)
            else:
                self.circle_right(radius, angle_degrees=180)
            radius += spacing 


