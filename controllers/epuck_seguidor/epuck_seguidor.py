#Imports

from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
vel_max = 2*3.14

#Motores
#Objeto
esq_motor = robot.getDevice('left wheel motor')
dir_motor = robot.getDevice('right wheel motor')
#Desliga controle de posição
esq_motor.setPosition(float('inf'))
dir_motor.setPosition(float('inf'))
#Ligar o controle de Velocidade
esq_motor.setVelocity(0.0)
dir_motor.setVelocity(0.0)

## Objetos dos sensores infravermelhos
esq_ir = robot.getDevice('ir2')
esq_ir.enable(timestep)
dir_ir = robot.getDevice('ir1')
dir_ir.enable(timestep)

#Velocidade do seguidor de linha
vel_esq = vel_max
vel_dir = vel_max
ganho=0.55

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    valor_ir_esq = esq_ir.getValue()
    valor_ir_dir = dir_ir.getValue()

    # Velocidade padrão    
    vel_esq = ganho*vel_max
    vel_dir = ganho*vel_max
    
    #print("esq: {}; dir: {}".format(valor_ir_esq,valor_ir_dir))
    
    if (valor_ir_esq > valor_ir_dir) and (6 < valor_ir_esq < 25):
        print('Indo à esquerda')
        vel_esq=-ganho*vel_max
        
    if (valor_ir_dir > valor_ir_esq) and (6 < valor_ir_dir < 25):
        print('Indo à direita')
        vel_dir=-ganho*vel_max
    
    
    esq_motor.setVelocity(vel_esq)
    dir_motor.setVelocity(vel_dir)
    
    
    pass

# Enter here exit cleanup code.
