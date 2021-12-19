import random
import simpy

# REVISAR SI LA MAQUINA ES UN NUMERO != 0 PARA SABER QUE HAY UNA MAQUINA AHI, EN EL CASO QUE SEA 0, SE SABE QUE NO HAY MAQUINA
# CREAR UN ARREGLO CON NÚMEROS DE LOS LUGARES VACIOS

tab = "             "

maquinasEnFabrica = []
maquinasDeRepuesto = []

cantidad = 8
reparadores = 3
tiempo = 


def maquinasEnFuncionamiento(env, counter, cantidadFab, cantidadRep):
    for i in range(cantidadFab):
        maquinasEnFabrica.append(i+1)

    for i in range(cantidadRep):
        maquinasDeRepuesto.append(i+1)

    for i in range(len(maquinasEnFabrica)):
        duracionArreglo = random.randrange(5, 11)
        c = repair(env, maquinasEnFabrica[i], counter, duracionArreglo)
        env.process(c)
        yield env.timeout(0)


def repair(env, name, counter, time_in_repair):
    arrive = env.now

    while True:
        
        duracionMaquina = random.randrange(130, 190)
        print('%10.0f %s %s: Funcionando ' % (arrive, tab, name))
        yield env.timeout(duracionMaquina)

        arrive = env.now
        print('%10.0f %s %s: Se dañó máquina ' % (arrive, tab, name))

        with counter.request() as req:
            # Wait for the counter or abort at the end of our tether
            results = yield req

            wait = env.now - arrive

            # We got to the counter
            print('%10.0f %s %s esperó en cola de reparación %1.0f horas' % (env.now, tab, name, wait))

            print('%10.0f %s %s: Me están arreglando' % (env.now, tab, name))

            yield env.timeout(time_in_repair)
            print('%10.0f %s %s: Terminaron de arreglarme' % (env.now, tab, name))

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
env.process(maquinasEnFuncionamiento(env, counter, cantidad, 0))
env.run(until = 360)