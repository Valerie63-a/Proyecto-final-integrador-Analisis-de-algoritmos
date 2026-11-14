from c1_merge_sort.merge_sort import merge_sort, ordenar_pedidos_por_plazo
from datos.generador import generar_pedidos, Pedido


def identidad(x):
    return x


def test_lista_vacia_y_un_elemento():
    assert merge_sort([], identidad) == []
    assert merge_sort([7], identidad) == [7]


def test_ya_ordenada_e_inversa():
    assert merge_sort([1, 2, 3, 4, 5], identidad) == [1, 2, 3, 4, 5]
    assert merge_sort([5, 4, 3, 2, 1], identidad) == [1, 2, 3, 4, 5]


def test_no_modifica_la_entrada():
    original = [3, 1, 2]
    merge_sort(original, identidad)
    assert original == [3, 1, 2]


def test_estabilidad_con_plazos_repetidos():
    pedidos = [Pedido(0, 0, 0, 5), Pedido(1, 0, 0, 3),
               Pedido(2, 0, 0, 5), Pedido(3, 0, 0, 3)]
    ordenados = ordenar_pedidos_por_plazo(pedidos)
    assert [p.id for p in ordenados] == [1, 3, 0, 2]


def test_contra_sorted_como_referencia():
    # sorted() se usa SOLO aquí, como referencia de comparación (permitido).
    for n in [0, 1, 2, 17, 100, 1000]:
        pedidos = generar_pedidos(n, semilla=n + 1)
        obtenido = ordenar_pedidos_por_plazo(pedidos)
        esperado = sorted(pedidos, key=lambda p: p.plazo)
        assert obtenido == esperado

def test_comparaciones_del_peor_caso_con_indices():
    # La versión con índices hace exactamente las mismas comparaciones:
    # entrada intercalada de n = 8 -> n·lg n - n + 1 = 17.
    contador = [0]
    merge_sort([0, 4, 2, 6, 1, 5, 3, 7], identidad, contador)
    assert contador[0] == 17
