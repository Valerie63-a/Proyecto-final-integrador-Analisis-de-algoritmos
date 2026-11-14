from typing import NamedTuple

from c1_merge_sort.merge_sort import ordenar_pedidos_por_plazo


class Tarea(NamedTuple):
    #Vista de una entrada del cronograma. Ya NO se crea una por pedido al
    #calcular: se construye solo cuando alguien la pide (pruebas, impresión).
    pedido: object
    inicio: int
    fin: int
    retraso: int  # fin - plazo (negativo si se entrega con holgura)


class Cronograma:
    #Cronograma de un repartidor guardado en arreglos paralelos.
    #Calcularlo no crea un objeto por pedido: solo escribe enteros en cuatro
    #listas reservadas de antemano y lleva el L_max en la misma pasada.
    __slots__ = ("pedidos", "inicios", "fines", "retrasos", "retraso_max")

    def __init__(self, pedidos, inicios, fines, retrasos, retraso_max):
        self.pedidos = pedidos
        self.inicios = inicios
        self.fines = fines
        self.retrasos = retrasos
        self.retraso_max = retraso_max

    def __len__(self):
        return len(self.pedidos)

    def __getitem__(self, i):
        return Tarea(self.pedidos[i], self.inicios[i], self.fines[i], self.retrasos[i])

    def __iter__(self):
        for i in range(len(self.pedidos)):
            yield self[i]

    def __eq__(self, otro):
        if isinstance(otro, (Cronograma, list, tuple)):
            return list(self) == list(otro)
        return NotImplemented


def servicio_unitario(pedido):
    #Duración por defecto: cada pedido toma 1 unidad de tiempo.
    return 1


def calcular_cronograma(secuencia, duracion=servicio_unitario):
    #Dada una secuencia de pedidos, calcula inicio, fin y retraso de cada uno.
    #El repartidor empieza en t = 0 y atiende sin pausas. Θ(n), una sola pasada,
    #sin crear tuplas por pedido (arreglos paralelos reservados una vez).
    pedidos = list(secuencia)
    n = len(pedidos)
    inicios = [0] * n
    fines = [0] * n
    retrasos = [0] * n
    tiempo = 0
    maximo = None
    for i in range(n):
        pedido = pedidos[i]
        inicios[i] = tiempo
        tiempo += duracion(pedido)
        fines[i] = tiempo
        retraso = tiempo - pedido.plazo
        retrasos[i] = retraso
        if maximo is None or retraso > maximo:
            maximo = retraso
    return Cronograma(pedidos, inicios, fines, retrasos, 0 if maximo is None else maximo)


def retraso_maximo(cronograma):
    #L_max = max(fin_i - plazo_i). Es la función objetivo que EDF minimiza.
    #Puede ser negativo (todos los pedidos salen con holgura). Lista vacía -> 0.
    if isinstance(cronograma, Cronograma):
        return cronograma.retraso_max          # calculado en la misma pasada
    if not cronograma:
        return 0
    maximo = cronograma[0].retraso
    for tarea in cronograma:
        if tarea.retraso > maximo:
            maximo = tarea.retraso
    return maximo


def planificar_edf(pedidos, duracion=servicio_unitario, ya_ordenados=False):
    #Voraz EDF (Earliest Deadline First): atiende primero el plazo más próximo.
    #Si los pedidos ya vienen ordenados por plazo (salida de C1), el costo es Θ(n);
    #si no, se ordenan con C1 y el total es Θ(n log n).
    #Devuelve el cronograma (Cronograma; se recorre como una lista de Tarea).
    if ya_ordenados:
        secuencia = pedidos
    else:
        secuencia = ordenar_pedidos_por_plazo(pedidos)
    return calcular_cronograma(secuencia, duracion)
