import math

from c1_merge_sort.merge_sort import merge_sort
from c5_arbol_r.ordenamiento_externo import ordenar_externo, pasadas_de_mezcla

# Formato de registro del disco: (id_o_hijo, xmin, ymin, xmax, ymax) = "qdddd".
# - Hoja: un punto es una caja degenerada (id, x, y, x, y).
# - Nodo interno: (bloque_hijo, caja envolvente del hijo).
# Un nodo ocupa exactamente un bloque (capacidad B registros).


def clave_x(entrada):
    return entrada[1] + entrada[3]   # 2 * centro en x


def clave_y(entrada):
    return entrada[2] + entrada[4]   # 2 * centro en y


def _empaquetar_rebanada(disco, rebanada):
    # Ordena la rebanada por y (C1), la corta en grupos de B y escribe un nodo
    # por grupo. Devuelve las entradas (bloque, caja) del nivel superior.
    B = disco.B
    ordenada = merge_sort(rebanada, clave_y)
    nuevas = []
    for desde in range(0, len(ordenada), B):
        grupo = ordenada[desde:desde + B]
        bloque = disco.reservar(1)
        disco.escribir_bloque(bloque, grupo)
        nuevas.append((bloque,
                       min(e[1] for e in grupo), min(e[2] for e in grupo),
                       max(e[3] for e in grupo), max(e[4] for e in grupo)))
    return nuevas


def _tam_rebanada(cantidad, B):
    nodos = math.ceil(cantidad / B)
    return math.ceil(math.sqrt(nodos)) * B   # S rebanadas verticales, S = ceil(sqrt(nodos))


def nodos_por_nivel(n, B):
    # Número de nodos de cada nivel, de las hojas a la raíz.
    cuentas = [math.ceil(n / B)]
    while cuentas[-1] > 1:
        cuentas.append(math.ceil(cuentas[-1] / B))
    return cuentas


def io_construccion_predichas(n, M, B):
    # Modelo de memoria externa. P = ceil(n/B) bloques de entrada.
    #   ordenar por x : P(1 + pasadas) lecturas y P(1 + pasadas) escrituras
    #   hojas         : P lecturas (rebanadas) y P escrituras (nodos hoja)
    #   niveles altos : U escrituras (en memoria, sin lecturas)
    P = math.ceil(n / B)
    pasadas = pasadas_de_mezcla(n, M, B)
    U = sum(nodos_por_nivel(n, B)[1:])
    lecturas = P * (1 + pasadas) + P
    escrituras = P * (1 + pasadas) + P + U
    return lecturas, escrituras


def io_consulta_esperadas(n, B, ancho, alto, lado):
    # Datos uniformes en [0, lado]^2. Un nodo del nivel con c nodos cubre una
    # región ~cuadrada de lado lado/sqrt(c); una consulta ancho x alto corta en
    # promedio (ancho/l + 1)(alto/l + 1) de ellos (como máximo c).
    total = 0.0
    for c in nodos_por_nivel(n, B):
        l = lado / math.sqrt(c)
        total += min(c, (ancho / l + 1) * (alto / l + 1))
    return total


class ArbolR:
    def __init__(self, disco, raiz, altura, n):
        self.disco = disco
        self.raiz = raiz
        self.altura = altura   # niveles: 1 = solo hoja
        self.n = n

    @staticmethod
    def construir_str(disco, inicio, n, M):
        # Carga masiva STR (Sort-Tile-Recursive). Los n puntos ya están en disco
        # desde el bloque 'inicio'. Requiere M >= ceil(n/B) y M >= S*B (una rebanada).
        B = disco.B
        if n == 0:
            return ArbolR(disco, None, 0, 0)
        hojas = math.ceil(n / B)
        tam = _tam_rebanada(n, B)
        if hojas > M or tam > M:
            raise ValueError("M insuficiente: se requiere M >= N/B y M >= sqrt(N*B)")

        ordenado = ordenar_externo(disco, inicio, n, clave_x, M)   # E/S: ordenar por x
        entradas = []
        for desde in range(0, n, tam):
            cuenta = min(tam, n - desde)
            rebanada = []
            for b in range(math.ceil(cuenta / B)):
                rebanada.extend(disco.leer_bloque(ordenado + desde // B + b))
            entradas.extend(_empaquetar_rebanada(disco, rebanada))

        altura = 1
        while len(entradas) > 1:   # niveles superiores, en memoria
            ordenadas = merge_sort(entradas, clave_x)
            tam = _tam_rebanada(len(ordenadas), B)
            nuevas = []
            for desde in range(0, len(ordenadas), tam):
                nuevas.extend(_empaquetar_rebanada(disco, ordenadas[desde:desde + tam]))
            entradas = nuevas
            altura += 1
        return ArbolR(disco, entradas[0][0], altura, n)

    def consultar(self, xmin, ymin, xmax, ymax):
        # Ids de los puntos dentro del rectángulo. Cada nodo visitado = 1 lectura.
        resultado = []
        if self.raiz is None:
            return resultado
        pila = [(self.raiz, 0)]
        while pila:
            bloque, nivel = pila.pop()
            entradas = self.disco.leer_bloque(bloque)
            if nivel == self.altura - 1:
                for e in entradas:
                    if xmin <= e[1] <= xmax and ymin <= e[2] <= ymax:
                        resultado.append(e[0])
            else:
                for e in entradas:
                    if e[1] <= xmax and e[3] >= xmin and e[2] <= ymax and e[4] >= ymin:
                        pila.append((e[0], nivel + 1))
        return resultado
