# vessel math
import math

# Set some basic stepper motor characteristics 
MOTOR_STEP_ANGLE = 1.8 # in degree
MICROSTEPPING = 16
STEPS_PER_REVOLUTION = MICROSTEPPING*360/MOTOR_STEP_ANGLE
# pipet stats
PIPET_OD = 4.9 # mm
PIPET_CIRCUMFERENCE = math.pi*PIPET_OD
INITIAL_Y_AXIS_STEPS_PER_MM = STEPS_PER_REVOLUTION/PIPET_CIRCUMFERENCE # steps per mm
# number of steps per mm for X,Y,Z,E axes
AXIS_STEPS_PER_MM = (101.01,INITIAL_Y_AXIS_STEPS_PER_MM,1600.00,3538.49)

# Move simulation
feedrate = 60.0 # mm/min
x = 5.0
y = 5.0
z = 0.0
dz = 0
e = 5

steps = (round(x*AXIS_STEPS_PER_MM[0]),round(y*AXIS_STEPS_PER_MM[1]),round(z*AXIS_STEPS_PER_MM[2]),round(e*AXIS_STEPS_PER_MM[3]))
disp_mm = (steps[0]/AXIS_STEPS_PER_MM[0],steps[1]/AXIS_STEPS_PER_MM[1],steps[2]/AXIS_STEPS_PER_MM[2],steps[3]/AXIS_STEPS_PER_MM[3])
r = math.sqrt(x**2+y**2+z**2)
z_height = PIPET_OD/2.0 + dz
total_move_time = 60.0*r/feedrate
move_angle = math.atan(y/x)
axes_speeds = (feedrate*math.cos(move_angle),feedrate*math.sin(move_angle),0,60.0*e/total_move_time) # mm/min
ysteprate = steps[1]/total_move_time # steps per second
angular_velocity = 2*math.pi*ysteprate/STEPS_PER_REVOLUTION # radians per second
tan_velocity = angular_velocity*z_height # mm per second

print("One full turn of the mandrel is: {} steps".format(STEPS_PER_REVOLUTION))
print("Axis steps per mm | X{0} Y{1} Z{2} E{3}".format(AXIS_STEPS_PER_MM[0],AXIS_STEPS_PER_MM[1],AXIS_STEPS_PER_MM[2],AXIS_STEPS_PER_MM[3]))
print("Move statistics:")
print("Input move (mm): X{0} Y{1} Z{2} E{3}".format(x,y,z,e))
print("Input feedrate: {0} mm/min | {1} mm/s".format(feedrate,feedrate/60.0))
print("Steps: X{0} Y{1} Z{2} E{3}".format(steps[0],steps[1],steps[2],steps[3]))
#print("Actual displacement: X{0} Y{1} Z{2} E{3}".format(disp_mm[0],disp_mm[1],disp_mm[2],disp_mm[3]))
print("Magnitude of move (mm): R{}".format(r))
print("Total move time (s): {}".format(total_move_time))
print("Axes speed (mm/min): X{0} Y{1} Z{2} E{3}".format(axes_speeds[0],axes_speeds[1],axes_speeds[2],axes_speeds[3]))
print("This would all be true if we were talking about a normal Cartesian move... But we are talking about a cylindrical geometry.")
print("")
print("The mandrel is move {} steps / {} steps of a full revolution in {} seconds.".format(steps[1],STEPS_PER_REVOLUTION,total_move_time))
print("The effective step rate of the mandrel is {} steps per second or {} degrees per second".format(ysteprate,360/(2*math.pi)*angular_velocity))
print("The tangential velocity of the nozzle head relative to the spinning mandrel is: {} mm/s.".format(tan_velocity))
print("As for the extrusion speed, it will be {} mm/min".format(axes_speeds[3]))
print("")
print("In summary, the X, theta, and E speeds will be: {0} mm/min | {1} mm/min | {2} mm/min".format(axes_speeds[0],60*tan_velocity,axes_speeds[3]))

