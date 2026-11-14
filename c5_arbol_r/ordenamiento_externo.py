import math

from c1_merge_sort.merge_sort import merge_sort
from comun.monton import MontonMinimo


def pasadas_de_mezcla(n, M, B):
    # Número de pasadas de mezcla: ceil(log_k(R)), con R corridas y k = M/B - 1.
    efectivo = (M // B) * B
    corridas = math.ceil(n / efectivo)
    k = efectivo // B - 1
    pasadas = 0
    while corridas > 1:
        corridas = math.ceil(corridas / k)
        pasadas += 1
    return pasadas


def ordenar_externo(disco, inicio, n, clave, M):
    # Ordenamiento externo por mezcla. Los n registros están en los bloques
    # inicio, inicio+1, ... Devuelve el índice del bloque donde queda el resultado.
    # Memoria: M registros (M/B bloques). Coste: 2*ceil(n/B)*(1 + pasadas) E/S.
    B = disco.B
    efectivo = (M // B) * B
    if efectivo // B < 3:
        raise ValueError("se necesitan al menos 3 bloques de memoria (M >= 3B)")
    k = efectivo // B - 1

    # Fase 1: corridas de M registros ordenadas en memoria con C1.
    corridas = []  # (bloque_inicial, registros)
    for desde in range(0, n, efectivo):
        cuenta = min(efectivo, n - desde)
        registros = []
        for b in range(math.ceil(cuenta / B)):
            registros.extend(disco.leer_bloque(inicio + desde // B + b))
        registros = merge_sort(registros, clave)
        destino = disco.reservar(math.ceil(cuenta / B))
        for b in range(math.ceil(cuenta / B)):
            disco.escribir_bloque(destino + b, registros[b * B:(b + 1) * B])
        corridas.append((destino, cuenta))

    # Fase 2: mezcla de k corridas por pasada, con un montículo propio.
    while len(corridas) > 1:
        nuevas = []
        for g in range(0, len(corridas), k):
            nuevas.append(_mezclar_grupo(disco, corridas[g:g + k], clave))
        corridas = nuevas
    return corridas[0][0] if corridas else disco.reservar(0)


def _mezclar_grupo(disco, grupo, clave):
    B = disco.B
    total = sum(cuenta for _, cuenta in grupo)
    destino = disco.reservar(math.ceil(total / B))
    buffers = []     # registros del bloque actual de cada corrida
    posicion = []    # siguiente registro a consumir
    siguiente = []   # siguiente bloque por leer
    restantes = []   # bloques que faltan por leer
    monton = MontonMinimo()
    for r, (bloque, cuenta) in enumerate(grupo):
        buffers.append(disco.leer_bloque(bloque))
        posicion.append(0)
        siguiente.append(bloque + 1)
        restantes.append(math.ceil(cuenta / B) - 1)
        monton.push((clave(buffers[r][0]), r))

    salida = []
    escritos = 0
    while len(monton):
        _, r = monton.pop()
        registro = buffers[r][posicion[r]]
        posicion[r] += 1
        salida.append(registro)
        if len(salida) == B:
            disco.escribir_bloque(destino + escritos, salida)
            escritos += 1
            salida = []
        if posicion[r] == len(buffers[r]) and restantes[r] > 0:
            buffers[r] = disco.leer_bloque(siguiente[r])
            siguiente[r] += 1
            restantes[r] -= 1
            posicion[r] = 0
        if posicion[r] < len(buffers[r]):
            monton.push((clave(buffers[r][posicion[r]]), r))
    if salida:
        disco.escribir_bloque(destino + escritos, salida)
    return (destino, total)
