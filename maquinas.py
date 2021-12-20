import random
import simpy

# REVISAR SI LA MAQUINA ES UN NUMERO != 0 PARA SABER QUE HAY UNA MAQUINA AHI, EN EL CASO QUE SEA 0, SE SABE QUE NO HAY MAQUINA
# CREAR UN ARREGLO CON NÚMEROS DE LOS LUGARES VACIOS

tab = "             "

maquinasEnFabrica = []
maquinasDeRepuesto = []
espaciosVacios = []

cantidadMaq = 5
maquinasFuncionando = 0
cantidadRep = 2
reparadores = 3
tiempo = 180

for i in range(cantidadMaq):
    maquinasEnFabrica.append(i+1)

for i in range(cantidadRep):
    maquinasDeRepuesto.append("Repuesto%02d" % i)

def maquinasEnFuncionamiento(env, counter):
    
    while len(maquinasEnFabrica) != 0:
        duracionArreglo = random.randrange(5, 11)
        c = repair(env, maquinasEnFabrica[0], counter, duracionArreglo)
        env.process(c)
        global maquinasFuncionando
        maquinasFuncionando += 1
        yield env.timeout(0)
        maquinasEnFabrica.pop(0)


def repair(env, name, counter, time_in_repair):
    arrive = env.now

    duracionMaquina = random.randrange(130, 190)    # Genera un número al azar para simular el tiempo de funcionamiento de la máquina
    print('%10.0f %s %s: Funcionando ' % (arrive, tab, name))
    yield env.timeout(duracionMaquina)

    arrive = env.now
    print('%10.0f %s %s: Se dañó máquina ' % (arrive, tab, name))
    espaciosVacios.append(name)     # Agrega la máquina que se acaba de dañar
    global maquinasFuncionando
    maquinasFuncionando -= 1

    print()
    print("Número de máquinas de repuesto disponibles: %s" % len(maquinasDeRepuesto))
    print()

    if len(maquinasDeRepuesto) != 0 and maquinasFuncionando != cantidadMaq:
        maquinasEnFabrica.append(maquinasDeRepuesto.pop(0))
        duracionArreglo = random.randrange(5, 11)
        c = repair(env, maquinasEnFabrica[0], counter, duracionArreglo)
        env.process(c)
        yield env.timeout(0)
        maquinasEnFabrica.pop(0)

    with counter.request() as req:
        results = yield req

        wait = env.now - arrive

        print()
        print("%s Maquinas en zona de reparación: %s" % (tab, espaciosVacios))
        print()

        # We got to the repair zonw
        print('%10.0f %s %s esperó en cola de reparación %1.0f horas' % (env.now, tab, name, wait))

        print('%10.0f %s %s: Me están arreglando' % (env.now, tab, name))
        yield env.timeout(time_in_repair)

        print('%10.0f %s %s: Terminaron de arreglarme' % (env.now, tab, name))
        espaciosVacios.pop(0) # Saca la máquina de la cola de máquinas en la sala de reparación

        arrive = env.now

        if len(maquinasDeRepuesto) == 0 and maquinasFuncionando != cantidadMaq:
            maquinasEnFabrica.append(name)
            duracionArreglo = random.randrange(5, 11)
            c = repair(env, maquinasEnFabrica[0], counter, duracionArreglo)
            env.process(c)
        else:
            maquinasDeRepuesto.append(name)


# Setup and start the simulation
print()
print(' ---------- Funcionamiento de paso a reparación ----------')
print()

espacio = "         "
print('Reloj de simulación %s Maquinas' % (espacio))
print()
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity = reparadores)
env.process(maquinasEnFuncionamiento(env, counter))
env.run(until = tiempo)