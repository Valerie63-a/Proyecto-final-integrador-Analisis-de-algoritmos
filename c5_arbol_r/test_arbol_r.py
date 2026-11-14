import math
import os
import random
import tempfile

import pytest

from c5_arbol_r.arbol_r import (ArbolR, io_construccion_predichas,
                                nodos_por_nivel)
from c5_arbol_r.ordenamiento_externo import ordenar_externo, pasadas_de_mezcla
from comun.disco_simulado import DiscoSimulado
from datos.generador import generar_puntos


@pytest.fixture
def ruta():
    carpeta = tempfile.mkdtemp()
    yield os.path.join(carpeta, "disco.bin")


def cargar(disco, registros):
    inicio = disco.reservar(math.ceil(len(registros) / disco.B))
    for b in range(math.ceil(len(registros) / disco.B)):
        disco.escribir_bloque(inicio + b, registros[b * disco.B:(b + 1) * disco.B])
    disco.reiniciar_contadores()
    return inicio


def puntos_como_registros(puntos):
    return [(i, x, y, x, y) for i, (x, y) in enumerate(puntos)]


def test_disco_lectura_escritura_y_contadores(ruta):
    disco = DiscoSimulado(ruta, 4)
    disco.escribir_bloque(0, [(1, 0.5, 1.5, 2.5, 3.5), (2, 0.0, 0.0, 0.0, 0.0)])
    disco.escribir_bloque(1, [])
    assert disco.leer_bloque(0) == [(1, 0.5, 1.5, 2.5, 3.5), (2, 0.0, 0.0, 0.0, 0.0)]
    assert disco.leer_bloque(1) == []
    assert (disco.lecturas, disco.escrituras) == (2, 2)
    with pytest.raises(IndexError):
        disco.leer_bloque(7)
    with pytest.raises(ValueError):
        disco.escribir_bloque(0, [(0, 0, 0, 0, 0)] * 5)
    disco.cerrar()


def test_ordenamiento_externo_ordena_y_cumple_la_formula(ruta):
    B, M, n = 4, 16, 1000      # 63 corridas, k = 3 -> 4 pasadas de mezcla
    generador = random.Random(1)
    registros = [(i, generador.random(), 0.0, 0.0, 0.0) for i in range(n)]
    disco = DiscoSimulado(ruta, B)
    inicio = cargar(disco, registros)
    resultado = ordenar_externo(disco, inicio, n, lambda r: r[1], M)
    salida = []
    for b in range(math.ceil(n / B)):
        salida.extend(disco.leer_bloque(resultado + b))
    assert [r[1] for r in salida] == sorted(r[1] for r in registros)
    P = math.ceil(n / B)
    pasadas = pasadas_de_mezcla(n, M, B)
    assert pasadas == 4
    # lecturas de la fase de ordenamiento: P(1 + pasadas); se restan las P de verificación
    assert disco.lecturas - P == P * (1 + pasadas)
    assert disco.escrituras == P * (1 + pasadas)
    disco.cerrar()


@pytest.mark.parametrize("n", [1, 3, 4, 5, 37, 200, 513])
def test_consulta_coincide_con_fuerza_bruta(ruta, n):
    B, M = 4, max(64, n)
    puntos = generar_puntos(n, semilla=n)
    disco = DiscoSimulado(ruta, B)
    inicio = cargar(disco, puntos_como_registros(puntos))
    arbol = ArbolR.construir_str(disco, inicio, n, M)
    generador = random.Random(n)
    for _ in range(25):
        x0, y0 = generador.uniform(0, 1000), generador.uniform(0, 1000)
        x1, y1 = x0 + generador.uniform(0, 400), y0 + generador.uniform(0, 400)
        esperado = sorted(i for i, (x, y) in enumerate(puntos)
                          if x0 <= x <= x1 and y0 <= y <= y1)
        assert sorted(arbol.consultar(x0, y0, x1, y1)) == esperado
    disco.cerrar()


def test_io_de_construccion_coincide_exactamente_con_la_formula(ruta):
    for n, B, M in [(200, 4, 64), (1000, 8, 200), (5000, 16, 400), (777, 5, 160)]:
        disco = DiscoSimulado(ruta, B)
        inicio = cargar(disco, puntos_como_registros(generar_puntos(n, semilla=3)))
        ArbolR.construir_str(disco, inicio, n, M)
        assert (disco.lecturas, disco.escrituras) == io_construccion_predichas(n, M, B)
        disco.cerrar()


def test_estructura_del_arbol(ruta):
    n, B = 1000, 8
    disco = DiscoSimulado(ruta, B)
    inicio = cargar(disco, puntos_como_registros(generar_puntos(n)))
    arbol = ArbolR.construir_str(disco, inicio, n, 200)
    assert arbol.altura == len(nodos_por_nivel(n, B))
    # consulta que cubre todo devuelve todos los puntos
    assert sorted(arbol.consultar(-1, -1, 2000, 2000)) == list(range(n))
    disco.cerrar()


def test_memoria_insuficiente_se_rechaza(ruta):
    disco = DiscoSimulado(ruta, 4)
    inicio = cargar(disco, puntos_como_registros(generar_puntos(200)))
    with pytest.raises(ValueError):
        ArbolR.construir_str(disco, inicio, 200, 16)
