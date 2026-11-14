from comun.geometria import distancia_euclidiana

# 2-aproximación para TSP métrico (distancia euclidiana).
# Convenciones iguales a C4: el punto 0 es el depósito; la ruta es un ciclo que
# empieza en 0 (el regreso a 0 es implícito) y se devuelve como lista de índices.


def arbol_expansion_minima(puntos, contador=None):
    # Prim en Θ(n²) sin montículo, calculando distancias al vuelo (espacio Θ(n)).
    # Devuelve (padre, peso): padre[v] es el padre de v en el árbol (padre[0] = -1).
    # contador: lista [0] opcional; cuenta las distancias evaluadas (n(n-1)/2).
    n = len(puntos)
    infinito = float("inf")
    en_arbol = [False] * n
    mejor = [infinito] * n
    padre = [-1] * n
    mejor[0] = 0.0
    peso = 0.0
    for _ in range(n):
        u = -1
        for v in range(n):
            if not en_arbol[v] and (u == -1 or mejor[v] < mejor[u]):
                u = v
        en_arbol[u] = True
        peso += mejor[u]
        for v in range(n):
            if not en_arbol[v]:
                if contador is not None:
                    contador[0] += 1
                distancia = distancia_euclidiana(puntos[u], puntos[v])
                if distancia < mejor[v]:
                    mejor[v] = distancia
                    padre[v] = u
    return padre, peso


def recorrido_preorden(padre):
    # Recorrido en profundidad (preorden) del árbol desde la raíz 0, iterativo.
    n = len(padre)
    hijos = [[] for _ in range(n)]
    for v in range(1, n):
        hijos[padre[v]].append(v)
    ruta = []
    pila = [0]
    while pila:
        u = pila.pop()
        ruta.append(u)
        for v in reversed(hijos[u]):   # para visitar los hijos en orden creciente
            pila.append(v)
    return ruta


def longitud_ruta(puntos, ruta):
    total = 0.0
    for k in range(len(ruta)):
        total += distancia_euclidiana(puntos[ruta[k]], puntos[ruta[(k + 1) % len(ruta)]])
    return total


def tsp_2_aproximado(puntos, contador=None):
    # Devuelve (longitud, ruta, peso_mst). Garantía: peso_mst <= OPT <= longitud <= 2*peso_mst.
    n = len(puntos)
    if n == 0:
        return 0.0, [], 0.0
    if n == 1:
        return 0.0, [0], 0.0
    padre, peso = arbol_expansion_minima(puntos, contador)
    ruta = recorrido_preorden(padre)
    return longitud_ruta(puntos, ruta), ruta, peso
