import random
from itertools import permutations

import pytest

from c4_ruta_optima.ruta_optima import (held_karp, backtracking,
                                        matriz_distancias, longitud_ciclo)
from datos.generador import generar_puntos


def fuerza_bruta(puntos):
    # Referencia: prueba todas las permutaciones (solo viable para n pequeño).
    n = len(puntos)
    d = matriz_distancias(puntos)
    mejor = float("inf")
    for resto in permutations(range(1, n)):
        longitud = longitud_ciclo([0] + list(resto), d)
        if longitud < mejor:
            mejor = longitud
    return mejor


def es_ruta_valida(ruta, n):
    return ruta[0] == 0 and sorted(ruta) == list(range(n))


ALGORITMOS = [
    pytest.param(held_karp, id="held_karp"),
    pytest.param(lambda p: backtracking(p, con_poda=True), id="backtracking_con_poda"),
    pytest.param(lambda p: backtracking(p, con_poda=False), id="backtracking_sin_poda"),
]


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_casos_pequenos(algoritmo):
    assert algoritmo([]) == (0.0, [])
    assert algoritmo([(5, 5)]) == (0.0, [0])
    longitud, ruta = algoritmo([(0, 0), (3, 4)])
    assert longitud == pytest.approx(10.0)  # ida y vuelta
    assert ruta == [0, 1]
    longitud, _ = algoritmo([(0, 0), (3, 0), (3, 4)])  # triángulo 3-4-5
    assert longitud == pytest.approx(12.0)


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_cuadrado_con_puntos_desordenados(algoritmo):
    # El perímetro del cuadrado (4.0) solo se logra recorriéndolo en orden.
    puntos = [(0, 0), (1, 1), (1, 0), (0, 1)]
    longitud, ruta = algoritmo(puntos)
    assert longitud == pytest.approx(4.0)
    assert es_ruta_valida(ruta, 4)


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_ruta_valida_y_longitud_coherente(algoritmo):
    puntos = generar_puntos(9, semilla=5)
    longitud, ruta = algoritmo(puntos)
    assert es_ruta_valida(ruta, 9)
    assert longitud == pytest.approx(longitud_ciclo(ruta, matriz_distancias(puntos)))


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_contra_fuerza_bruta(algoritmo):
    for semilla in range(15):
        n = random.Random(semilla).randint(2, 8)
        puntos = generar_puntos(n, semilla=semilla)
        longitud, _ = algoritmo(puntos)
        assert longitud == pytest.approx(fuerza_bruta(puntos))


def test_backtracking_coincide_con_held_karp():
    for semilla in range(10):
        puntos = generar_puntos(10, semilla=100 + semilla)
        optimo, _ = held_karp(puntos)
        con_poda, _ = backtracking(puntos, con_poda=True)
        assert con_poda == pytest.approx(optimo)


def test_puntos_repetidos():
    puntos = [(0, 0), (0, 0), (10, 0), (10, 0)]
    for algoritmo in (held_karp, backtracking):
        longitud, ruta = algoritmo(puntos)
        assert longitud == pytest.approx(20.0)
        assert es_ruta_valida(ruta, 4)


def test_no_modifica_la_entrada():
    puntos = generar_puntos(7, semilla=2)
    copia = list(puntos)
    held_karp(puntos)
    backtracking(puntos)
    assert puntos == copia


def test_held_karp_cuenta_transiciones_exactas():
    # Hay m·(m-1)·2^(m-2) transiciones (i -> j), con m = n - 1.
    for n in [3, 4, 6, 9]:
        m = n - 1
        contador = [0]
        held_karp(generar_puntos(n), contador)
        assert contador[0] == m * (m - 1) * 2 ** (m - 2)


def test_backtracking_sin_poda_recorre_todo_el_arbol():
    # En el nivel k hay m!/(m-k)! nodos, con m = n - 1.
    n = 6
    m = n - 1
    esperado = 0
    fijo = 1
    for k in range(m + 1):
        esperado += fijo  # m!/(m-k)!
        fijo *= m - k
    assert esperado == 326
    contador = [0]
    backtracking(generar_puntos(n), con_poda=False, contador=contador)
    assert contador[0] == esperado


def test_la_poda_reduce_los_nodos_explorados():
    puntos = generar_puntos(10, semilla=3)
    sin_poda = [0]
    con_poda = [0]
    backtracking(puntos, con_poda=False, contador=sin_poda)
    backtracking(puntos, con_poda=True, contador=con_poda)
    assert con_poda[0] < sin_poda[0] / 10
