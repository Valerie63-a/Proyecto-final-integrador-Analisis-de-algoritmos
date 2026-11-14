#Funciones de medición compartidas por todos los scripts de experimentos.
#Antes cada script tenía su propia copia de pendiente_loglog; ahora hay una sola.

import gc
import math
import statistics
import time


def pendiente_loglog(xs, ys):
    #Pendiente de la recta log(y) vs log(x) por mínimos cuadrados.
    #Si y = c·x^k, la pendiente es k (1 = lineal, 2 = cuadrático).
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    numerador = sum((a - mx) * (b - my) for a, b in zip(lx, ly))
    denominador = sum((a - mx) ** 2 for a in lx)
    return numerador / denominador


def cronometrar(funcion, *argumentos):
    #Una ejecución medida con perf_counter y el recolector de basura apagado
    #(como hace timeit), para que una recolección no caiga dentro de la medición.
    gc.disable()
    try:
        inicio = time.perf_counter()
        resultado = funcion(*argumentos)
        return time.perf_counter() - inicio, resultado
    finally:
        gc.enable()


def medir(funcion, *argumentos, repeticiones=5):
    #Mediana y desviación estándar (s) de varias ejecuciones de funcion(*argumentos).
    tiempos = [cronometrar(funcion, *argumentos)[0] for _ in range(repeticiones)]
    return statistics.median(tiempos), statistics.pstdev(tiempos)
