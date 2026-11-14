def merge_sort(elementos, clave, contador=None):
    #Devuelve una lista nueva ordenada ascendentemente según clave(elemento).
    #contador: lista [0] opcional; cuenta comparaciones entre claves.
    #
    #Implementación con índices: no se usa slicing (elementos[:mitad]) en la
    #recursión. Se trabaja sobre UNA copia de la entrada y UN arreglo auxiliar
    #del mismo tamaño, reservados una sola vez, y cada llamada recibe los
    #límites [inicio, fin). Espacio auxiliar Θ(n) + Θ(log n) de pila.
    arreglo = list(elementos)      # copia de trabajo: la entrada no se modifica
    n = len(arreglo)
    if n <= 1:
        return arreglo
    auxiliar = [None] * n
    _ordenar(arreglo, auxiliar, 0, n, clave, contador)
    return arreglo


def _ordenar(arreglo, auxiliar, inicio, fin, clave, contador):
    #Ordena arreglo[inicio:fin] en su lugar. T(n) = 2T(n/2) + Θ(n).
    if fin - inicio <= 1:
        return
    mitad = inicio + (fin - inicio) // 2
    _ordenar(arreglo, auxiliar, inicio, mitad, clave, contador)
    _ordenar(arreglo, auxiliar, mitad, fin, clave, contador)
    _mezclar(arreglo, auxiliar, inicio, mitad, fin, clave, contador)


def _mezclar(arreglo, auxiliar, inicio, mitad, fin, clave, contador=None):
    #Mezcla los tramos ordenados arreglo[inicio:mitad] y arreglo[mitad:fin]
    #usando el arreglo auxiliar compartido (estable: en empate gana la izquierda).
    for k in range(inicio, fin):
        auxiliar[k] = arreglo[k]
    i = inicio
    j = mitad
    k = inicio
    while i < mitad and j < fin:
        if contador is not None:
            contador[0] += 1
        if clave(auxiliar[i]) <= clave(auxiliar[j]):
            arreglo[k] = auxiliar[i]
            i += 1
        else:
            arreglo[k] = auxiliar[j]
            j += 1
        k += 1
    while i < mitad:
        arreglo[k] = auxiliar[i]
        i += 1
        k += 1
    while j < fin:
        arreglo[k] = auxiliar[j]
        j += 1
        k += 1


def ordenar_pedidos_por_plazo(pedidos, contador=None):
    #Atajo para el caso del proyecto: ordena pedidos por su plazo.
    return merge_sort(pedidos, lambda pedido: pedido.plazo, contador)
