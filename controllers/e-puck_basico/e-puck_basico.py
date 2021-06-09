"""e-puck_basico controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
vel_max = 6.28

mot_esq = robot.getDevice('left wheel motor')
mot_esq.setPosition(float('inf'))
mot_esq.setVelocity(0.0)

mot_dir = robot.getDevice('right wheel motor')
mot_dir.setPosition(float('inf'))
mot_dir.setVelocity(0.0)


# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    mot_esq.setVelocity(0.5*vel_max)
    mot_dir.setVelocity(vel_max)
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    #pass

# Enter here exit cleanup code.
