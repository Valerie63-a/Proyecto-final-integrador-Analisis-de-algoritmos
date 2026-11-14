#Experimento C1: validación empírica de T(n) = 2T(n/2) + Θ(n).

#Hipótesis:
#H1: comparaciones C(n) entre (n/2)·log2(n) y n·log2(n) - n + 1 en todo caso.
#H2: pendiente log-log del tiempo ≈ 1 (ligeramente > 1 por el factor log n).
#H3: T(n)/(n log n) tiende a una constante.
#Protocolo: 8 tamaños (n se duplica), 5 repeticiones, mediana y dispersión (rango
#intercuartil aproximado), generación de datos fuera del tiempo medido.

import math
import statistics

from c1_merge_sort.merge_sort import ordenar_pedidos_por_plazo
from datos.generador import generar_pedidos
from experimentos.utilidades import cronometrar, pendiente_loglog

REPETICIONES = 5



def medir(n):
    tiempos = []
    contador = [0]
    for rep in range(REPETICIONES):
        pedidos = generar_pedidos(n, semilla=1000 + rep)  # fuera del tiempo medido
        tiempo, _ = cronometrar(ordenar_pedidos_por_plazo, pedidos)
        tiempos.append(tiempo)
    contador = [0]
    ordenar_pedidos_por_plazo(generar_pedidos(n, semilla=1000), contador)  # conteo aparte
    return statistics.median(tiempos), max(tiempos) - min(tiempos), contador[0]


def main():
    tamanos, medianas = [], []
    print(f"{'n':>8} {'mediana(s)':>11} {'rango(s)':>10} {'comparac.':>10} "
          f"{'n·lg n - n+1':>13} {'T/(n lg n) µs':>14}")
    n = 1000
    for _ in range(8):
        mediana, rango, comps = medir(n)
        techo = n * math.log2(n) - n + 1
        print(f"{n:>8} {mediana:>11.5f} {rango:>10.5f} {comps:>10} "
              f"{techo:>13.0f} {mediana / (n * math.log2(n)) * 1e6:>14.4f}")
        tamanos.append(n)
        medianas.append(mediana)
        n *= 2
    print(f"\nPendiente log-log estimada: {pendiente_loglog(tamanos, medianas):.3f}")


if __name__ == "__main__":
    main()
