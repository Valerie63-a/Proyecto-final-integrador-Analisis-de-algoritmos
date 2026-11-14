from c1_merge_sort.merge_sort import merge_sort
from comun.geometria import distancia_euclidiana

# Convenciones de C4:
# - puntos es una lista de (x, y); el punto 0 es el depósito.
# - Una ruta es un ciclo: sale de 0, visita todos los puntos una vez y regresa a 0.
#   Se devuelve como lista de índices que empieza en 0 (el regreso a 0 es implícito).
# - Ambas funciones devuelven (longitud, ruta).
# - n = len(puntos) incluye al depósito. Held-Karp aplica para n <= 16.


def matriz_distancias(puntos):
    # Matriz simétrica n x n con la distancia euclidiana entre cada par. Θ(n²).
    n = len(puntos)
    matriz = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            distancia = distancia_euclidiana(puntos[i], puntos[j])
            matriz[i][j] = distancia
            matriz[j][i] = distancia
    return matriz


def longitud_ciclo(ruta, d):
    # Longitud del ciclo que recorre ruta y regresa a su primer punto.
    total = 0.0
    for k in range(len(ruta)):
        total += d[ruta[k]][ruta[(k + 1) % len(ruta)]]
    return total


def held_karp(puntos, contador=None):
    # Programación dinámica de Held-Karp.
    # Subproblema: g(S, j) = longitud mínima de un camino que sale del depósito (0),
    # visita exactamente los puntos del conjunto S y termina en j (j en S).
    #   g({j}, j) = d(0, j)
    #   g(S, j)   = min sobre i en S\{j} de g(S\{j}, i) + d(i, j)
    # Respuesta: min sobre j de g(todos, j) + d(j, 0).
    # S se codifica como máscara de bits sobre los puntos 1..n-1 (bit k = punto k+1).
    # Tiempo Θ(n²·2ⁿ), espacio Θ(n·2ⁿ).
    # contador: lista [0] opcional; cuenta las transiciones (i -> j) evaluadas.
    n = len(puntos)
    if n == 0:
        return 0.0, []
    if n == 1:
        return 0.0, [0]

    d = matriz_distancias(puntos)
    m = n - 1  # puntos distintos del depósito
    total = 1 << m
    infinito = float("inf")
    g = [[infinito] * m for _ in range(total)]
    padre = [[-1] * m for _ in range(total)]

    for j in range(m):
        g[1 << j][j] = d[0][j + 1]

    # Los subconjuntos se recorren en orden numérico: S\{j} < S siempre,
    # así que cuando se necesita g(S\{j}, i) ya fue calculado.
    for S in range(1, total):
        for j in range(m):
            if not (S >> j) & 1:
                continue
            anterior = S ^ (1 << j)
            if anterior == 0:
                continue  # caso base, ya inicializado
            mejor = infinito
            mejor_i = -1
            for i in range(m):
                if (anterior >> i) & 1:
                    if contador is not None:
                        contador[0] += 1
                    costo = g[anterior][i] + d[i + 1][j + 1]
                    if costo < mejor:
                        mejor = costo
                        mejor_i = i
            g[S][j] = mejor
            padre[S][j] = mejor_i

    completo = total - 1
    mejor_longitud = infinito
    ultimo = -1
    for j in range(m):
        costo = g[completo][j] + d[j + 1][0]
        if costo < mejor_longitud:
            mejor_longitud = costo
            ultimo = j

    # Reconstrucción: se sigue la cadena de padres desde el último punto.
    inversa = []
    S = completo
    j = ultimo
    while j != -1:
        inversa.append(j + 1)
        siguiente = padre[S][j]
        S ^= 1 << j
        j = siguiente
    ruta = [0] + inversa[::-1]
    return mejor_longitud, ruta


def backtracking(puntos, con_poda=True, contador=None):
    # Backtracking: explora el árbol de permutaciones de los puntos 1..n-1.
    # Sin poda recorre todo el árbol: O(n!) en el peor caso.
    # Con poda: si (longitud parcial + cota inferior del resto) >= mejor ruta conocida,
    # se descarta la rama completa.
    #   Cota inferior: cada arista restante entra a un punto aún no visitado o al
    #   depósito, y cuesta al menos la arista más corta que llega a ese punto
    #   (min_entrada). La suma de esos mínimos no puede superar lo que falta.
    # La cota inicial es una ruta del vecino más cercano.
    # contador: lista [0] opcional; cuenta los nodos del árbol visitados.
    n = len(puntos)
    if n == 0:
        return 0.0, []
    if n == 1:
        return 0.0, [0]

    d = matriz_distancias(puntos)
    # Vecinos de cada punto ordenados por distancia (con C1, sin sorted).
    # Explorar primero lo cercano encuentra buenas rutas pronto y poda más.
    vecinos = []
    for u in range(n):
        otros = [v for v in range(n) if v != u]
        vecinos.append(merge_sort(otros, lambda v, u=u: d[u][v]))
    min_entrada = [d[v][vecinos[v][0]] for v in range(n)]

    mejor_longitud = float("inf")
    mejor_ruta = []
    if con_poda:
        # Ruta inicial por vecino más cercano (cota superior válida).
        visitado = [False] * n
        visitado[0] = True
        ruta_inicial = [0]
        longitud = 0.0
        actual = 0
        for _ in range(n - 1):
            for v in vecinos[actual]:
                if not visitado[v]:
                    break
            visitado[v] = True
            ruta_inicial.append(v)
            longitud += d[actual][v]
            actual = v
        mejor_longitud = longitud + d[actual][0]
        mejor_ruta = ruta_inicial

    visitado = [False] * n
    visitado[0] = True
    ruta = [0]

    def explorar(actual, parcial, cota_resto):
        nonlocal mejor_longitud, mejor_ruta
        if contador is not None:
            contador[0] += 1
        if len(ruta) == n:
            total = parcial + d[actual][0]
            if total < mejor_longitud:
                mejor_longitud = total
                mejor_ruta = list(ruta)
            return
        for v in vecinos[actual]:
            if visitado[v]:
                continue
            nuevo = parcial + d[actual][v]
            nueva_cota = cota_resto - min_entrada[v]
            if con_poda and nuevo + nueva_cota >= mejor_longitud:
                continue
            visitado[v] = True
            ruta.append(v)
            explorar(v, nuevo, nueva_cota)
            ruta.pop()
            visitado[v] = False

    cota_inicial = min_entrada[0]
    for v in range(1, n):
        cota_inicial += min_entrada[v]
    explorar(0, 0.0, cota_inicial)
    return mejor_longitud, mejor_ruta
