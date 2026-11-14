import random
from itertools import permutations

from c1_merge_sort.merge_sort import ordenar_pedidos_por_plazo
from c3_voraz.edf import (planificar_edf, calcular_cronograma, retraso_maximo,
                          Tarea)
from datos.generador import generar_pedidos, Pedido


def test_lista_vacia_y_un_pedido():
    assert planificar_edf([]) == []
    assert retraso_maximo([]) == 0
    cronograma = planificar_edf([Pedido(0, 0, 0, 5)])
    assert cronograma == [Tarea(Pedido(0, 0, 0, 5), 0, 1, -4)]


def test_orden_por_plazo_y_tiempos_consecutivos():
    pedidos = [Pedido(0, 0, 0, 9), Pedido(1, 0, 0, 2), Pedido(2, 0, 0, 5)]
    cronograma = planificar_edf(pedidos)
    assert [t.pedido.id for t in cronograma] == [1, 2, 0]
    assert [(t.inicio, t.fin) for t in cronograma] == [(0, 1), (1, 2), (2, 3)]
    assert [t.retraso for t in cronograma] == [-1, -3, -6]


def test_retraso_positivo_cuando_no_alcanza_el_tiempo():
    # Tres pedidos con plazo 1: el último termina en t = 3 -> retraso 2.
    pedidos = [Pedido(i, 0, 0, 1) for i in range(3)]
    assert retraso_maximo(planificar_edf(pedidos)) == 2


def test_acepta_lista_ya_ordenada_por_c1():
    pedidos = generar_pedidos(200, semilla=3)
    ordenados = ordenar_pedidos_por_plazo(pedidos)
    assert planificar_edf(ordenados, ya_ordenados=True) == planificar_edf(pedidos)


def test_no_modifica_la_entrada():
    pedidos = generar_pedidos(50, semilla=1)
    copia = list(pedidos)
    planificar_edf(pedidos)
    assert pedidos == copia


def test_duraciones_distintas():
    pedidos = [Pedido(0, 0, 0, 10), Pedido(1, 0, 0, 4)]
    duraciones = {0: 6, 1: 3}
    cronograma = planificar_edf(pedidos, duracion=lambda p: duraciones[p.id])
    assert [t.pedido.id for t in cronograma] == [1, 0]
    assert [(t.inicio, t.fin) for t in cronograma] == [(0, 3), (3, 9)]
    assert retraso_maximo(cronograma) == -1


def _optimo_por_fuerza_bruta(pedidos, duracion):
    # Prueba todas las permutaciones: solo viable para n pequeño.
    mejor = None
    for permutacion in permutations(pedidos):
        valor = retraso_maximo(calcular_cronograma(permutacion, duracion))
        if mejor is None or valor < mejor:
            mejor = valor
    return mejor


def test_optimalidad_contra_fuerza_bruta_duracion_unitaria():
    for semilla in range(40):
        n = random.Random(semilla).randint(1, 7)
        pedidos = generar_pedidos(n, semilla=semilla)
        obtenido = retraso_maximo(planificar_edf(pedidos))
        assert obtenido == _optimo_por_fuerza_bruta(pedidos, lambda p: 1)


def test_optimalidad_contra_fuerza_bruta_duraciones_aleatorias():
    for semilla in range(40):
        generador = random.Random(semilla)
        n = generador.randint(1, 7)
        pedidos = generar_pedidos(n, semilla=semilla)
        duraciones = {p.id: generador.randint(1, 10) for p in pedidos}
        duracion = lambda p: duraciones[p.id]
        obtenido = retraso_maximo(planificar_edf(pedidos, duracion))
        assert obtenido == _optimo_por_fuerza_bruta(pedidos, duracion)


def test_retraso_maximo_se_calcula_en_la_misma_pasada():
    pedidos = generar_pedidos(300, semilla=9)
    cronograma = planificar_edf(pedidos)
    assert retraso_maximo(cronograma) == max(t.retraso for t in cronograma)
    assert len(cronograma) == 300
