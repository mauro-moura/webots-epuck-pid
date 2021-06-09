#Imports
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
vel_max = 2*3.14

#Motores
esq_motor = robot.getDevice('left wheel motor')
dir_motor = robot.getDevice('right wheel motor')
#Desliga controle de posição
esq_motor.setPosition(float('inf'))
dir_motor.setPosition(float('inf'))
#Ligar o controle de Velocidade
esq_motor.setVelocity(0.0)
dir_motor.setVelocity(0.0)

## Objetos dos sensores infravermelhos
# Sensor da direita
sensor_1 = robot.getDevice('ir1')
sensor_1.enable(timestep)
# Sensor do meio
sensor_2 = robot.getDevice('ir0')
sensor_2.enable(timestep)
# Sensor da esquerda
sensor_3 = robot.getDevice('ir2')
sensor_3.enable(timestep)

# PID
last_error = intg = diff = prop = waitCounter = 0
# Erros anteriores   0.5
kp = 0.4
# Erros anteriores   0.0001
ki = 0
# Erros anteriores   0.35
kd = 0.35

# Para os Ks anteriores:
# Velocidade Máxima estável vel_max - 1.35
# Para os Ks atuais vel_max - 1.15 
#base_speed = vel_max - 1.15
base_speed = vel_max - 1.15

counter = 0

def get_error(sensor):
    if ((sensor[0] == 1) and (sensor[1] == 0) and (sensor[2] == 0)):
        # Totalmente a esquerda
        return 2
    elif ((sensor[0] == 1) and (sensor[1] == 1) and (sensor[2] == 0)):
        # Levemente a esquerda
        return 1
    elif ((sensor[0] == 0) and (sensor[1] == 1) and (sensor[2] == 0)):
        # Centralizado
        return 0
    elif ((sensor[0] == 0) and (sensor[1] == 1) and (sensor[2] == 1)):
        # Levemente a direita
        return -1
    elif ((sensor[0] == 0) and (sensor[1] == 0) and (sensor[2] == 1)):
        # Totalmente a direita
        return -2
    elif ((sensor[0] == 0) and (sensor[1] == 0) and (sensor[2] == 0)):
        # Robô fora da pista
        return 404
    else:
        return 3

def correct_sensor(sensor_value, color_min = 6, color_max = 25):
    if (color_min < sensor_value < color_max):
        return 1
    return 0

def pid(error):
    global last_error, intg, diff, prop, kp, ki, kd
    prop = error
    intg = error + intg
    diff = error - last_error
    balance = (kp*prop) + (ki*intg) + (kd*diff)
    last_error = error
    return balance

def path_finding(error, timeLimit = 200):
    global counter
    print(counter)
    if(counter < timeLimit):
        counter += 1
        setSpeed(base_speed, 0)
    elif (counter < timeLimit + 60):
        counter += 1
        setSpeed(base_speed, base_speed)
        esq_motor.setVelocity(vel_max)
        dir_motor.setVelocity(0)
    else:
        counter = 0

def setSpeed(base_speed, balance, max_speed = 6.28):
    vel_esq = min(max(-max_speed, base_speed + balance), max_speed)
    print("Velocidade da Esquerda: ", vel_esq)
    esq_motor.setVelocity(vel_esq)
    vel_dir = min(max(-max_speed, base_speed - balance), max_speed)
    print("Velocidade da Direita: ", vel_dir)
    dir_motor.setVelocity(vel_dir)

def car_control():
    global counter
    
    sensor_1_val = sensor_1.getValue()
    sensor_2_val = sensor_2.getValue()
    sensor_3_val = sensor_3.getValue()
    
    sensores = [sensor_1_val, sensor_2_val, sensor_3_val]
    
    print("Sensores normais: " + str(sensores))
    
    for i in range(len(sensores)):
        sensores[i] = correct_sensor(sensores[i])
    
    print("Sensores normalizados: " + str(sensores))
    error = get_error(sensores)

    if (error != 404):
        counter = 0
        rectify = pid(error)
        print("Valor do PID: " + str(rectify))
        setSpeed(base_speed, rectify)
    else:
        path_finding(error)

def turn_by(time = 40):
    delta = 3
    if (time > 0):
        print("Girando na %i vez"%(time))
        setSpeed(vel_max - delta, vel_max - delta)
        turn_by(time - 1)
    else:
        return 2

while robot.step(timestep) != -1:
    car_control()
    pass
