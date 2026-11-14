import gc
import math
import os
import random
import statistics
import tempfile
import time

from c5_arbol_r.arbol_r import (ArbolR, io_construccion_predichas,
                                io_consulta_esperadas)
from comun.disco_simulado import DiscoSimulado
from datos.generador import generar_puntos

B = 64                   # registros por bloque
LADO = 1000.0            # lado de la ciudad
LADO_CONSULTA = 100.0    # rectángulo de consulta: 1 % del área
CONSULTAS = 200
TAMANOS = [100_000, 150_000, 225_000, 337_500, 506_250, 759_375]   # razón 1,5


def cargar_entrada(disco, puntos):
    # Deja los puntos en disco como (id, x, y, x, y); esta carga NO cuenta como E/S.
    registros = [(i, x, y, x, y) for i, (x, y) in enumerate(puntos)]
    inicio = disco.reservar(math.ceil(len(registros) / B))
    for b in range(math.ceil(len(registros) / B)):
        disco.escribir_bloque(inicio + b, registros[b * B:(b + 1) * B])
    disco.reiniciar_contadores()
    return inicio


def medir_tamano(n, carpeta):
    M = n // 20
    puntos = generar_puntos(n, semilla=42)          # generación fuera del tiempo medido
    disco = DiscoSimulado(os.path.join(carpeta, f"disco_{n}.bin"), B)
    inicio = cargar_entrada(disco, puntos)
    gc.disable()
    t0 = time.perf_counter()
    arbol = ArbolR.construir_str(disco, inicio, n, M)
    tiempo = time.perf_counter() - t0
    gc.enable()
    construccion = (M, disco.lecturas, disco.escrituras, tiempo, arbol.altura)

    generador = random.Random(7)
    lecturas, resultados = [], []
    for _ in range(CONSULTAS):
        x0 = generador.uniform(0, LADO - LADO_CONSULTA)
        y0 = generador.uniform(0, LADO - LADO_CONSULTA)
        antes = disco.lecturas
        ids = arbol.consultar(x0, y0, x0 + LADO_CONSULTA, y0 + LADO_CONSULTA)
        lecturas.append(disco.lecturas - antes)
        resultados.append(len(ids))
    # Verificación contra fuerza bruta en una consulta.
    ids = arbol.consultar(300.0, 300.0, 300.0 + LADO_CONSULTA, 300.0 + LADO_CONSULTA)
    esperado = sum(1 for (x, y) in puntos if 300 <= x <= 300 + LADO_CONSULTA
                   and 300 <= y <= 300 + LADO_CONSULTA)
    assert len(ids) == esperado
    disco.cerrar()
    return construccion, lecturas, resultados


def main():
    carpeta = tempfile.mkdtemp()
    filas = [(n,) + medir_tamano(n, carpeta) for n in TAMANOS]

    print("=== Construcción STR: E/S contadas vs predichas (B = 64, M = N/20) ===")
    print(f"{'N':>8} {'M':>7} {'lect':>8} {'lect pred':>10} {'escr':>8} "
          f"{'escr pred':>10} {'tiempo (s)':>11} {'altura':>7}")
    for n, (M, lect, escr, tiempo, altura), _, _ in filas:
        lect_p, escr_p = io_construccion_predichas(n, M, B)
        print(f"{n:>8} {M:>7} {lect:>8} {lect_p:>10} {escr:>8} {escr_p:>10} "
              f"{tiempo:>11.2f} {altura:>7}")

    print("\n=== Consulta por rectángulo (1 % del área, 200 consultas por tamaño) ===")
    print(f"{'N':>8} {'E/S med':>8} {'E/S min':>8} {'E/S max':>8} {'E/S pred':>9} "
          f"{'resultados':>11} {'T/B':>7}")
    for n, _, lecturas, resultados in filas:
        pred = io_consulta_esperadas(n, B, LADO_CONSULTA, LADO_CONSULTA, LADO)
        t_medio = statistics.mean(resultados)
        print(f"{n:>8} {statistics.mean(lecturas):>8.1f} {min(lecturas):>8} "
              f"{max(lecturas):>8} {pred:>9.1f} {t_medio:>11.0f} {t_medio / B:>7.1f}")


if __name__ == "__main__":
    main()
