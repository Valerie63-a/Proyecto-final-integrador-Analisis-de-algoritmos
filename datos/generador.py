import random
from typing import NamedTuple

#C1
class Pedido(NamedTuple):
    id: int
    x: float
    y: float
    plazo: int


def generar_pedidos(n, semilla=42, lado_ciudad=1000.0):
    # Genera n pedidos con posición aleatoria y plazo entero en [1, 10n].
    # La semilla fija hace que los datos sean idénticos en cada ejecución.
    generador = random.Random(semilla)
    pedidos = []
    for identificador in range(n):
        x = generador.uniform(0, lado_ciudad)
        y = generador.uniform(0, lado_ciudad)
        plazo = generador.randint(1, 10 * n)
        pedidos.append(Pedido(identificador, x, y, plazo))
    return pedidos

#C2 
class EstadoVehiculo(NamedTuple):
    x: float
    y: float
    carga: int


def generar_vehiculos(m, semilla=7, lado_ciudad=1000.0, carga_maxima=100):
    #Devuelve m pares (id_vehiculo, EstadoVehiculo) con datos reproducibles.
    generador = random.Random(semilla)
    vehiculos = []
    for identificador in range(m):
        estado = EstadoVehiculo(
            generador.uniform(0, lado_ciudad),
            generador.uniform(0, lado_ciudad),
            generador.randint(0, carga_maxima),
        )
        vehiculos.append((identificador, estado))
    return vehiculos

#C4-C6
def generar_puntos(n, semilla=11, lado_ciudad=1000.0):
    # Devuelve n puntos (x, y) reproducibles en [0, lado_ciudad]^2.
    # El punto 0 hace de depósito: la ruta de C4 sale de él y regresa a él.
    generador = random.Random(semilla)
    puntos = []
    for _ in range(n):
        x = generador.uniform(0, lado_ciudad)
        y = generador.uniform(0, lado_ciudad)
        puntos.append((x, y))
    return puntos
