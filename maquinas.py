import random
import simpy

tab = "             "

maquinasEnFabrica = []
maquinasDeRepuesto = []
espaciosVacios = []

cantidadMaq = 5
maquinasFuncionando = 0
cantidadRep = 2
reparadores = 3
tiempo = 360

for i in range(cantidadMaq):
    maquinasEnFabrica.append(i+1)

for i in range(cantidadRep):
    maquinasDeRepuesto.append("Repuesto%02d" % i)

def maquinasEnFuncionamiento(env, counter):

    global maquinasFuncionando
    
    while len(maquinasEnFabrica) != 0:
        duracionArreglo = random.uniform(5, 11)
        c = repair(env, maquinasEnFabrica[0], counter, duracionArreglo)
        env.process(c)
        
        maquinasFuncionando += 1
        yield env.timeout(0)
        maquinasEnFabrica.pop(0)


def repair(env, name, counter, time_in_repair):

    arrive = env.now
    global maquinasFuncionando

    if(type(name) == int):
        duracionMaquina = random.uniform(130, 190)    # Genera un número al azar para simular el tiempo de funcionamiento de la máquina
    else:
        duracionMaquina = random.uniform(190, 250)

    print('%10.0f %s %s: Funcionando ' % (arrive, tab, name))
    yield env.timeout(duracionMaquina)

    print()
    print("Máquinas funcionando en la fábrica: %s" % maquinasFuncionando)
    print()

    arrive = env.now
    print('%10.0f %s %s: Se dañó máquina ' % (arrive, tab, name))
    espaciosVacios.append(name)     # Agrega la máquina que se acaba de dañar
    
    maquinasFuncionando -= 1

    print()
    print("Máquinas de repuesto disponibles: %s" % maquinasDeRepuesto)
    print()

    if len(maquinasDeRepuesto) != 0 and maquinasFuncionando != cantidadMaq:
        maquinasEnFabrica.append(maquinasDeRepuesto.pop(0))
        duracionArreglo = random.uniform(5, 11)
        c = repair(env, maquinasEnFabrica[0], counter, duracionArreglo)
        env.process(c)
        yield env.timeout(0)
        maquinasEnFabrica.pop(0)
        maquinasFuncionando += 1

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
            duracionArreglo = random.uniform(5, 11)
            c = repair(env, maquinasEnFabrica[0], counter, duracionArreglo)
            env.process(c)
            maquinasFuncionando += 1
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