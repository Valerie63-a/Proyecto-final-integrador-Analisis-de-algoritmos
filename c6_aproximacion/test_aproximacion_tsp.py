import math

import pytest

from c4_ruta_optima.ruta_optima import held_karp
from c6_aproximacion.aproximacion_tsp import (arbol_expansion_minima,
                                              recorrido_preorden,
                                              tsp_2_aproximado)
from datos.generador import generar_puntos

TOLERANCIA = 1e-9


def test_casos_pequenos():
    assert tsp_2_aproximado([]) == (0.0, [], 0.0)
    assert tsp_2_aproximado([(3, 4)]) == (0.0, [0], 0.0)
    longitud, ruta, peso = tsp_2_aproximado([(0, 0), (3, 4)])
    assert ruta == [0, 1] and math.isclose(longitud, 10.0) and math.isclose(peso, 5.0)


def test_mst_de_puntos_alineados():
    # Sobre una recta, el MST es la cadena y pesa la distancia total.
    puntos = [(0, 0), (10, 0), (3, 0), (7, 0)]
    padre, peso = arbol_expansion_minima(puntos)
    assert math.isclose(peso, 10.0)
    assert sorted(recorrido_preorden(padre)) == [0, 1, 2, 3]


@pytest.mark.parametrize("n", [3, 8, 40, 200])
def test_ruta_valida(n):
    puntos = generar_puntos(n, semilla=n)
    _, ruta, _ = tsp_2_aproximado(puntos)
    assert ruta[0] == 0 and sorted(ruta) == list(range(n))


def test_garantia_contra_held_karp():
    # w(MST) <= OPT <= longitud <= 2 * w(MST) y por tanto longitud <= 2 * OPT.
    for n in range(4, 11):
        for semilla in range(10):
            puntos = generar_puntos(n, semilla=1000 * n + semilla)
            optimo, _ = held_karp(puntos)
            longitud, _, peso = tsp_2_aproximado(puntos)
            assert peso <= optimo + TOLERANCIA
            assert optimo <= longitud + TOLERANCIA
            assert longitud <= 2 * peso + TOLERANCIA
            assert longitud <= 2 * optimo + TOLERANCIA


def test_cuenta_exacta_de_distancias():
    for n in (2, 10, 57):
        contador = [0]
        tsp_2_aproximado(generar_puntos(n), contador)
        assert contador[0] == n * (n - 1) // 2


def test_no_modifica_la_entrada():
    puntos = generar_puntos(12)
    copia = list(puntos)
    tsp_2_aproximado(puntos)
    assert puntos == copia
