import math
import statistics

from c4_ruta_optima.ruta_optima import held_karp, backtracking
from datos.generador import generar_puntos
from experimentos.utilidades import cronometrar as _cronometrar


def cronometrar(funcion, *argumentos):
    # Solo el tiempo (s) de una ejecución; la medición vive en experimentos/utilidades.py.
    return _cronometrar(funcion, *argumentos)[0]

REPETICIONES = 5



def nodos_sin_poda(n):
    # Nodos del árbol de permutaciones: suma de m!/(m-k)! para k = 0..m, con m = n - 1.
    m = n - 1
    total = 0
    fijo = 1
    for k in range(m + 1):
        total += fijo
        fijo *= m - k
    return total


def experimento_held_karp():
    print("=== Held-Karp: Θ(n²·2ⁿ) tiempo (5 repeticiones sobre los mismos datos) ===")
    print(f"{'n':>3} {'T med (s)':>10} {'sigma':>9} {'T/(n²·2ⁿ) ns':>14} "
          f"{'T(n)/T(n-1)':>12} {'trans. cont.':>13} {'m(m-1)2^(m-2)':>14}")
    anterior = None
    for n in range(6, 17):
        puntos = generar_puntos(n)  # generación fuera del tiempo medido
        tiempos = [cronometrar(held_karp, puntos) for _ in range(REPETICIONES)]
        mediana = statistics.median(tiempos)
        contador = [0]
        held_karp(puntos, contador)  # corrida aparte: el contador altera el tiempo
        m = n - 1
        esperado = m * (m - 1) * 2 ** (m - 2)
        razon = "" if anterior is None else f"{mediana / anterior:.2f}"
        print(f"{n:>3} {mediana:>10.5f} {statistics.pstdev(tiempos):>9.5f} "
              f"{mediana / (n * n * 2 ** n) * 1e9:>14.2f} {razon:>12} "
              f"{contador[0]:>13} {esperado:>14}")
        anterior = mediana
    print("Si la teoría es correcta, T/(n²·2ⁿ) tiende a una constante y")
    print("T(n)/T(n-1) ronda 2·(n/(n-1))² (≈ 2.2 - 2.9 en este rango).\n")


def experimento_backtracking_sin_poda():
    print("=== Backtracking SIN poda: O(n!) (5 repeticiones sobre los mismos datos) ===")
    print(f"{'n':>3} {'T med (s)':>10} {'sigma':>9} {'nodos cont.':>12} "
          f"{'nodos teoría':>13} {'T/nodo (us)':>12} {'T(n)/T(n-1)':>12}")
    anterior = None
    for n in range(5, 11):
        puntos = generar_puntos(n)
        tiempos = [cronometrar(backtracking, puntos, False) for _ in range(REPETICIONES)]
        mediana = statistics.median(tiempos)
        contador = [0]
        backtracking(puntos, False, contador)
        razon = "" if anterior is None else f"{mediana / anterior:.2f}"
        print(f"{n:>3} {mediana:>10.5f} {statistics.pstdev(tiempos):>9.5f} "
              f"{contador[0]:>12} {nodos_sin_poda(n):>13} "
              f"{mediana / contador[0] * 1e6:>12.3f} {razon:>12}")
        anterior = mediana
    print("T(n)/T(n-1) crece con n (≈ n-1 cuando n es grande): comportamiento factorial.\n")


def experimento_backtracking_con_poda():
    print("=== Backtracking CON poda: 5 instancias distintas por tamaño (semillas 0-4) ===")
    print("La poda depende de los datos, por eso se varía la instancia en vez de repetir una.")
    print(f"{'n':>3} {'T med (s)':>10} {'T min':>8} {'T max':>8} {'nodos med':>11} "
          f"{'nodos sin poda':>15} {'% explorado':>12}  óptimo = Held-Karp")
    for n in range(6, 17):
        tiempos = []
        nodos = []
        coincide = True
        for semilla in range(REPETICIONES):
            puntos = generar_puntos(n, semilla=semilla)
            optimo, _ = held_karp(puntos)
            contador = [0]
            longitud, _ = backtracking(puntos, True, contador)  # cuenta nodos
            nodos.append(contador[0])
            tiempos.append(cronometrar(backtracking, puntos, True))
            coincide = coincide and math.isclose(longitud, optimo, rel_tol=1e-9)
        sin_poda = nodos_sin_poda(n)
        mediana_nodos = statistics.median(nodos)
        print(f"{n:>3} {statistics.median(tiempos):>10.5f} {min(tiempos):>8.4f} "
              f"{max(tiempos):>8.4f} {mediana_nodos:>11.0f} {sin_poda:>15} "
              f"{mediana_nodos / sin_poda * 100:>11.5f}%  {'sí' if coincide else 'NO'}")
    print()


def main():
    experimento_held_karp()
    experimento_backtracking_sin_poda()
    experimento_backtracking_con_poda()


if __name__ == "__main__":
    main()
