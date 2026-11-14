#C1: mejor, peor y caso esperado de merge sort medidos en comparaciones.

# Para n = 2^k:  mejor = (n/2)·lg n (ordenada o inversa),
               #peor  = n·lg n - n + 1 (entrada intercalada),
               #esperado (aleatoria) ≈ n·lg n - 1.25·n.

import math

from c1_merge_sort.merge_sort import merge_sort
from datos.generador import generar_pedidos


def identidad(x):
    return x


def peor_entrada(valores):
    # Separa posiciones pares/impares recursivamente: fuerza que cada mezcla
    # compare hasta agotar una de las dos mitades.
    if len(valores) <= 1:
        return list(valores)
    return peor_entrada(valores[0::2]) + peor_entrada(valores[1::2])


def comparaciones(lista):
    contador = [0]
    merge_sort(lista, identidad, contador)
    return contador[0]


def main():
    print(f"{'n':>7} {'mejor':>9} {'(n/2)lg n':>10} {'aleatoria':>10} "
          f"{'peor':>9} {'n lg n-n+1':>11}")
    n = 1024
    for _ in range(6):
        lg = int(math.log2(n))
        mejor = comparaciones(list(range(n)))
        inversa = comparaciones(list(range(n, 0, -1)))
        aleatoria = comparaciones([p.plazo for p in generar_pedidos(n, semilla=5)])
        peor = comparaciones(peor_entrada(list(range(n))))
        assert mejor == inversa == (n // 2) * lg
        assert peor == n * lg - n + 1
        print(f"{n:>7} {mejor:>9} {(n // 2) * lg:>10} {aleatoria:>10} "
              f"{peor:>9} {n * lg - n + 1:>11}")
        n *= 2


if __name__ == "__main__":
    main()
