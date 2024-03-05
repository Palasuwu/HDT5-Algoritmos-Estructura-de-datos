#HTD5 Algoritmos y estructuras de Datos 
#Jorge Palacios
import simpy
import random
import math
from random import seed
seed(56)
        
#Simpy enviroment 
env = simpy.Environment()
CPU = simpy.Resource(env, capacity=2)
RAM = simpy.Container(env, init=100, capacity=100)
ramProcess = 0
instructions = 0
Cambioinstructions= 6# Changes instructions per procces
listCPU = list()
tiempoPromedio = 0
process_Quantity = 200
interval= 1# No 0

def Process(name, env,  cpu, ram):
    global tiempoPromedio
    tempRam = random.randint(1,10)
    instructions = random.randint(1,10)
    yield env.timeout(random.expovariate(1.0/interval)) #Generates new Process
    
    #Ram ------------------------------
    with RAM.get(tempRam) as queueForRam:
        yield queueForRam
        print('Process %s is in new state at %s' % (name, env.now))
        print('Process %s requested %s of RAM' % (name, tempRam))
        ramProcess = tempRam
        print(RAM.level,"RAM available")

        #CPU ---------
        yield env.timeout(0.5)
        print('Process %s is in Ready mode at %s' % (name, env.now))
        print('Process %s requested the CPU' %(name))
        print('Process %s has %s instructions' %(name, instructions))
        while(instructions > 0):
            with CPU.request() as req:
                yield req
                print('Process %s is running now' % (name))
                if((instructions - 3) <= Cambioinstructions): 
                    yield env.timeout((1/instructions) * instructions)
                    instructions = instructions - instructions
                    print('Process %s is Terminated at %s' %(name, env.now))
                    tiempoPromedio = env.now
                    listCPU.append(env.now)
                    RAM.put(ramProcess) 
                else:
                    yield env.timeout(1)
                    instructions = instructions - 3 
                    print('Process %s leaves the CPU at %s' % (name, env.now))
                    io = random.randint(1,2)
                    if io == 1:
                        print('Process %s is in waiting state' % (name))
                        yield env.timeout(1)
                    else:
                        print('Process %s is in ready state' % (name))
                        print('Process %s has %s instructions left' % (name, instructions ))
        

#New Processes 
def procesar () :
   for i in range(process_Quantity):
     env.process(Process(i, env, CPU, RAM))

     yield env.timeout(random.expovariate(1.0 / interval))
env.process(procesar())  
env.run()

#Data
def calcular_promedio(lista):
  suma = 0
  for valor in lista:
    suma += valor
  return suma / len(lista)

def calcular_desviacion_estandar(lista):
  promedio = calcular_promedio(lista)
  varianza = 0
  for valor in lista:
    varianza += (valor - promedio) ** 2
  desviacion_estandar = math.sqrt(varianza / len(lista))
  return desviacion_estandar

tiempoPromedio = calcular_promedio(listCPU)
desvest = calcular_desviacion_estandar(listCPU)
print("                           ")
print("Cantidad de procesos: ", process_Quantity)
print("--------------------------------")
print("                           ")
print("El tiempo promedio ", tiempoPromedio)
print("--------------------------------")

print("Desviacion estandar: ", desvest)
print("--------------------------------")


print("Finish :D ")
