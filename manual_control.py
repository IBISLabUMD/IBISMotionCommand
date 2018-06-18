def manual_control(mc, distance=0.1, velocity=0.2):
    ctrl_token = ''
    print('a = left, d = right, w = forward, s = back, 1 = turn left, 2 = turn\
          right, k = up, j = down, q = quit')
    while ctrl_token != 'q':
        ctrl_token = input('Provide Control Token:')
        if ctrl_token == 'a':
            mc.left(distance, velocity)
        elif ctrl_token == 'd':
            mc.right(distance, velocity)
        elif ctrl_token == 'w':
            mc.forward(distance, velocity)
        elif ctrl_token == 's':
            mc.back(distance, velocity)
        elif ctrl_token == '1':
            mc.turn_left(10, 10)
        elif ctrl_token == '2':
            mc.turn_right(10, 10)
        elif ctrl_token == 'k':
            mc.up(distance, velocity)
        elif ctrl_token == 'j':
            mc.down(distance, velocity)
        else:
            mc.stop()
