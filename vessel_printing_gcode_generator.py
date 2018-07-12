import math

# Set some basic stepper motor characteristics 
MOTOR_STEP_ANGLE = 1.8 # in degree
MICROSTEPPING = 16
STEPS_PER_REVOLUTION = MICROSTEPPING*360/MOTOR_STEP_ANGLE

# Pipet dictionary
PIPET = '1 mL'
P_DICT = {'1 mL':4.95,'2 mL':5.6,'5 mL':8.9,}
# Set up characteristics about the pipet
PIPET_OD = P_DICT[PIPET] # mm
PIPET_CIRCUMFERENCE = math.pi*PIPET_OD # mm
INITIAL_Y_AXIS_STEPS_PER_MM = STEPS_PER_REVOLUTION/PIPET_CIRCUMFERENCE # steps per mm


# Syringe dictionary of diameters (mm)
SYRINGE = '3 mL'
S_DICT = {'1 mL':4.78,'3 mL':8.46,'5 mL':12.06}

SYRINGE_DIAMETER= S_DICT[SYRINGE] # mm
CROSS_SECTIONAL_AREA = math.pi*(SYRINGE_DIAMETER/2)**2

# Calculated statistics
# number of steps per mm for X,Y,Z,E axes
AXIS_STEPS_PER_MM = (101.01,INITIAL_Y_AXIS_STEPS_PER_MM,1600.00,3538.49)
# Minimum travel distance for each axes
MIN_DIST = tuple([1./axes for axes in AXIS_STEPS_PER_MM])


############## USER-INPUT ################
# Inputs that work are: vessel_length = 18, layer_thickness = 1, z_clearance = 0.6, revs_per_mm = 2, print_speed = 100, num_layers = 2
vessel_length = 10 # mm
layer_thickness = 1 # mm
z_clearance = 0.60 # mmm
num_layers = 3
print_speed = 500 # mm/min
revs_per_mm = 2
retraction_speed = 100 # mm/min

########## Invariable parameters ##########
revs_per_layer = vessel_length*revs_per_mm
vessel_thickness = layer_thickness*num_layers
vessel_volume = vessel_length*math.pi*vessel_thickness*(vessel_thickness+PIPET_OD)
# For calculating layer volume
# From Mathematica: V = (pi/4)*L*((dOD + 2*dz)^2 - dOD^2)
# Simplified: V = L*pi*dz*(dz + dOD)
layer_volume = vessel_length*math.pi*layer_thickness*(layer_thickness+PIPET_OD)
extrusion_length = layer_volume/CROSS_SECTIONAL_AREA
direction = 1 # 1 = positive x-direction | -1 = negative x_direction

if __name__ == "__main__":

	print(";Printing with a {syringe_name} syringe on a {pipet_name} pipet...".format(syringe_name=SYRINGE,pipet_name=PIPET))
	print(";{syringe_name} syringe (diameter X uL/mm): ({diameter:.4f} mm X {V_mm:.4f} uL/mm)".format(syringe_name=SYRINGE,diameter=SYRINGE_DIAMETER,V_mm=CROSS_SECTIONAL_AREA))
	print(";{pipet_name} pipet (OD X circumference): ({OD:.4f} mm X {circumference:.4f}) mm.".format(pipet_name=PIPET,OD=PIPET_OD,circumference=PIPET_CIRCUMFERENCE))
	print(';Min. travel/extrusion distance (mm): X{:.4f} Y{:.4f} Z{:.4f} E{:.4f}.'.format(MIN_DIST[0],MIN_DIST[1],MIN_DIST[2],MIN_DIST[3]))
	print(';Min. extrudable volume: {:.4f} uL.'.format(MIN_DIST[3]*CROSS_SECTIONAL_AREA))
	print(';Revolutions per mm: {} | Revolutions per layer: {}'.format(revs_per_mm,revs_per_layer))
	print(';Vessel dimensions - Lumenal diameter: {} mm | Wall thickness: {} mm | Length: {} mm'.format(PIPET_OD,vessel_thickness,vessel_length))
	print(';Total volume required per vessel graft: {:.1f} uL'.format(vessel_volume))
	print(";Move syringe tip to the 0.0 mL line before starting.")

	print('')

	print('M92 X{} Z{} E{}'.format(AXIS_STEPS_PER_MM[0],AXIS_STEPS_PER_MM[2],AXIS_STEPS_PER_MM[3]))
	#print('M302 P1 ;Turn off cold extrusion protection')
	print('G92 X0 Y0')
	print('G91')
	print('G1 F{}'.format(print_speed))
	print('G1 Z{}'.format(-z_clearance))
	print('M203 X1000 Y1000 E1000') # override max feedrates
	print('')

	prev_layer_diameter = PIPET_OD
	for layer in range(num_layers):

		layer_diameter = (PIPET_OD + 2*layer_thickness*(layer+1)) # influenced by loop
		layer_circumference = math.pi*layer_diameter
		y_axis_steps_per_mm = STEPS_PER_REVOLUTION/layer_circumference
		layer_volume = (math.pi/4)*vessel_length*(layer_diameter**2 - prev_layer_diameter**2)
		extrusion_length = layer_volume/CROSS_SECTIONAL_AREA
		circum_travel_distance = layer_circumference*revs_per_layer
		direction = 1*(-1)**layer # influenced by loop

		print(";Preparing to print layer #{} ...".format(layer+1)) # influenced by loop
		print(";Volume of this layer: {} uL".format(layer_volume))
		print(";Extrusion length for this layer: {} mm".format(extrusion_length))
		print(";Circumferential travel distance: {} mm".format(circum_travel_distance))
		print(";Axis steps per mm for this layer: {} mm".format(y_axis_steps_per_mm))
		print(";Printing layer #{} ...".format(layer+1)) # influenced by 
		print("M92 Y{}".format(y_axis_steps_per_mm))
		print('G91')
		print('G1 F{}'.format(print_speed))
		print("G28 Y ; Home Y axis")
		print ("G1 X{} Y{} E{}".format(direction*vessel_length,circum_travel_distance,extrusion_length))
		if layer != num_layers-1:
			print("G1 Z{}".format(-z_clearance))
		print('')

		prev_layer_diameter = layer_diameter

	print(';Send printer to next section')
	for i in range(2):
		print('G1 Z-1')
		print('G4 P1000')
	print('G1 X30 F500')
	print('G1 E-15 F{}'.format(retraction_speed))


# startting with 1.0 ml at 0.72 mL line and gel at 1.0 mL syringe opening. put 24G tip on.
# pushed gel to opening of tip. now gel at 0.57 mL.