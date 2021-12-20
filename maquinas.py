import random
import simpy

tab = "             "
espacio = "         "

# VARIABLES QUE SIRVEN PARA EL FUNCIONAMIENTO DE LA SIMULACION
maquinasEnFabrica = []
maquinasDeRepuesto = []
maquinasDañadas = []
maquinasFuncionando = 0
tiempoSinAlgunaMaquina = 0
tiempoDesdeVacio = 0


# VARIABLES A MODIFICAR
# CON ESTOS VALORES, SE CUMPLE REGULARMENTE LA CONDICIÓN DE QUE LA CAPACIDAD DEBE DE SER DE ENTRE 93% Y 96%
cantidadMaq = 50
cantidadRep = 15
reparadores = 4
tiempo = 720

for i in range(cantidadMaq):
    maquinasEnFabrica.append(i+1)

for i in range(cantidadRep):
    maquinasDeRepuesto.append("Repuesto%02d" % i)

def maquinasEnFuncionamiento(env, repairman):

    global maquinasFuncionando
    
    while len(maquinasEnFabrica) != 0:
        duracionArreglo = random.uniform(5, 11)
        c = repair(env, maquinasEnFabrica[0], repairman, duracionArreglo)
        env.process(c)
        
        maquinasFuncionando += 1
        yield env.timeout(0.01)
        maquinasEnFabrica.pop(0)


def repair(env, name, repairman, time_in_repair):

    arrive = env.now
    global maquinasFuncionando
    global tiempoSinAlgunaMaquina
    global tiempoDesdeVacio

    # Esta es la variante 2. La variante original es sin el if y solo con el generador entre 130 y 190
    # Genera un número al azar para simular el tiempo de funcionamiento de la máquina
    #if(type(name) == int):
    duracionMaquina = random.uniform(130, 190)    
    #else:
        #duracionMaquina = random.uniform(190, 250)

    # SIMULA CUANDO UNA MAQUINA ESTÁ FUNCIONANDO
    #print('%10.0f %s %s: Funcionando ' % (arrive, tab, name))
    yield env.timeout(duracionMaquina)

    """print()
                print("Máquinas funcionando en la fábrica: %s" % maquinasFuncionando)
                print()"""

    arrive = env.now

    # SIMULA CUANDO UNA MAQUINA SE DAÑA
    #print('%10.0f %s %s: Se dañó máquina ' % (arrive, tab, name))
    maquinasDañadas.append(name) # AGREGA LA MAQUINA A LA LISTA DE MAQUINAS DAÑADAS
    maquinasFuncionando -= 1

    """print()
                print("Máquinas de repuesto disponibles: %s" % maquinasDeRepuesto)
                print()"""

    # CUENTA DESDE QUE MOMENTO LA FABRICA ESTA TRABAJANDO A MENOR CAPACIDAD
    if len(maquinasDeRepuesto) == 0 and maquinasFuncionando != cantidadMaq and tiempoDesdeVacio == 0:
        tiempoDesdeVacio = env.now
        #print("Tiempo desde que hay un vacio en la fábrica: %d" % tiempoDesdeVacio)

    # AGREGA MAQUINAS DE REPUESTO A LA FABRICA
    if len(maquinasDeRepuesto) != 0 and maquinasFuncionando != cantidadMaq:
        maquinasEnFabrica.append(maquinasDeRepuesto.pop(0))
        duracionArreglo = random.uniform(5, 11)
        c = repair(env, maquinasEnFabrica.pop(0), repairman, duracionArreglo)
        env.process(c)
        yield env.timeout(0)
        maquinasFuncionando += 1

    """print()
                print("Máquinas funcionando en la fábrica: %s" % maquinasFuncionando)
                print("Máquinas que deben estar en la fábrica: %s" % cantidadMaq)
                print()"""

    with repairman.request() as req:
        results = yield req

        wait = env.now - arrive

        """print()
                                print("%s Maquinas en zona de reparación: %s" % (tab, maquinasDañadas))
                                print()"""

        # ZONA DE REPARACIÓN
        #print('%10.0f %s %s esperó en cola de reparación %1.0f horas' % (env.now, tab, name, wait))

        #print('%10.0f %s %s: Me están arreglando' % (env.now, tab, name))
        yield env.timeout(time_in_repair)

        #print('%10.0f %s %s: Terminaron de arreglarme' % (env.now, tab, name))
        maquinasDañadas.pop(0) # SACA LA MÁQUINA DE LA COLA DE MÁQUINAS EN LA SALA DE REPARACIÓN

        arrive = env.now

        if len(maquinasDeRepuesto) == 0 and maquinasFuncionando != cantidadMaq:
            maquinasEnFabrica.append(name)
            duracionArreglo = random.uniform(5, 11)
            c = repair(env, maquinasEnFabrica.pop(0), repairman, duracionArreglo)
            maquinasFuncionando += 1

            # MIRA CUÁNDO DESPUÉS DE QUE SE FORMA UN "HUECO", VUELVEN A HABER 50 MAQUINAS FUNCIONANDO
            if maquinasFuncionando == cantidadMaq and tiempoDesdeVacio != 0:
                tiempoSinAlgunaMaquina += round(arrive, 0) - round(tiempoDesdeVacio, 0)
                tiempoDesdeVacio = 0

            env.process(c)

        else:
            maquinasDeRepuesto.append(name)


# Setup and start the simulation
"""print()
print(' ---------- Funcionamiento de paso a reparación ----------')
print()"""

#print('Reloj de simulación %s Maquinas' % (espacio))
#print()
env = simpy.Environment()

# Start processes and run
repairman = simpy.Resource(env, capacity = reparadores)
env.process(maquinasEnFuncionamiento(env, repairman))
env.run(until = tiempo)

print()
print("Horas con menos de %d máquinas funcionando: %d" % (maquinasFuncionando, tiempoSinAlgunaMaquina))
porcentajeConVacio = (tiempoSinAlgunaMaquina / tiempo) * 100
capacidad = 100 - porcentajeConVacio
mensajeCap = "Es decir que la capacidad de producción fue del %d" % (round(capacidad, 2))
print(mensajeCap + "%")
print()

"""pruebas = 15
arregloValores = []

def correrSim():
    

for i in range(pruebas):
    env = simpy.Environment()
    repairman = simpy.Resource(env, capacity = reparadores)
    env.process(maquinasEnFuncionamiento(env, repairman))
    env.run(until = tiempo)
    print(tiempoSinAlgunaMaquina)
    porcentajeConVacio = (tiempoSinAlgunaMaquina / tiempo) * 100
    capacidad = round(100 - porcentajeConVacio, 2)
    arregloValores.append(capacidad)"""

#print(arregloValores)