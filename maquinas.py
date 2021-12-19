import random
import simpy

# REVISAR SI LA MAQUINA ES UN NUMERO != 0 PARA SABER QUE HAY UNA MAQUINA AHI, EN EL CASO QUE SEA 0, SE SABE QUE NO HAY MAQUINA
# CREAR UN ARREGLO CON NÚMEROS DE LOS LUGARES VACIOS

tab = "             "

maquinasEnFabrica = []
maquinasDeRepuesto = []
espaciosVacios = []

cantidadMaq = 8
cantidadRep = 3
reparadores = 3
tiempo = 360


def maquinasEnFuncionamiento(env, counter, cantidadFab, cantidadRep):
    for i in range(cantidadFab):
        maquinasEnFabrica.append(i+1)

    for i in range(cantidadRep):
        maquinasDeRepuesto.append("Repuesto%02d" % i)

    for i in range(len(maquinasEnFabrica)):
        duracionArreglo = random.randrange(5, 11)
        c = repair(env, maquinasEnFabrica[i], counter, duracionArreglo)
        env.process(c)
        yield env.timeout(0)


def repair(env, name, counter, time_in_repair):
    arrive = env.now

    while True:
        
        duracionMaquina = random.randrange(130, 190)    # Genera un número al azar para simular el tiempo de funcionamiento de la máquina
        print('%10.0f %s %s: Funcionando ' % (arrive, tab, name))
        yield env.timeout(duracionMaquina)

        arrive = env.now
        print('%10.0f %s %s: Se dañó máquina ' % (arrive, tab, name))
        espaciosVacios.append(name)     # Agrega el indice del espacios vacío que dejó la máquina que se acaba de dañar

        with counter.request() as req:
            results = yield req

            wait = env.now - arrive

            print("%s %s" % (tab, espaciosVacios))

            # We got to the counter
            print('%10.0f %s %s esperó en cola de reparación %1.0f horas' % (env.now, tab, name, wait))

            print('%10.0f %s %s: Me están arreglando' % (env.now, tab, name))
            yield env.timeout(time_in_repair)

            print('%10.0f %s %s: Terminaron de arreglarme' % (env.now, tab, name))
            espaciosVacios.pop(0) # Saca el primer indice de los espacios vacíos para simular que la máquina vuelve a ese espacios

            arrive = env.now


# Setup and start the simulation
print()
print(' ---------- Funcionamiento de paso a reparación ----------')
print()

espacio = "         "
print('Reloj de simulación %s Maquinas' % (espacio))
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity = reparadores)
env.process(maquinasEnFuncionamiento(env, counter, cantidadMaq, cantidadRep))
env.run(until = tiempo)