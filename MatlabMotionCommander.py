from cflib.positioning.motion_commander import MotionCommander
import cflib.crtp
import matlab.engine

URI = 'radio://0/80/250K'
eng=matlab.engine.start_matlab()

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# Initialize the low-level drivers (don't list the debug drivers)
cflib.crtp.init_drivers(enable_debug_driver=False)
# The values that indicate where the crazyflie thinks it is
log_vars = ['kalman.stateX', 'kalman.stateY', 'kalman.stateZ']
# Where to print logging values
log_file = 'crazyflie_data.txt'

with MotionCommander(URI, log_file=log_file, log_vars=log_vars) as mc:
    # Add Motion Actions Here
    mc.up(0.3)
    mc.forward(0.3)
    mc.down(0.3)
    arr = cl.dump()
    mat_arr = double(arr)    
    print(mat_arr)
    # matlab function below
    s_est=eng.Spiral_Localization(mat_arr, nargout=2)
    print(s_est)
    sequence=[(s_est[0],s_est[1],0.4,0)]
    time.sleep(1)
    run_sequence(scf, sequence)
    time.sleep(3)
