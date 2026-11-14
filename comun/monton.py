class MontonMinimo:
    # Montículo binario mínimo propio (sin heapq). Guarda tuplas comparables.
    # push y pop: O(log n).

    def __init__(self):
        self.datos = []

    def __len__(self):
        return len(self.datos)

    def push(self, elemento):
        datos = self.datos
        datos.append(elemento)
        i = len(datos) - 1
        while i > 0:
            padre = (i - 1) // 2
            if datos[padre] <= datos[i]:
                break
            datos[padre], datos[i] = datos[i], datos[padre]
            i = padre

    def pop(self):
        datos = self.datos
        minimo = datos[0]
        ultimo = datos.pop()
        if datos:
            datos[0] = ultimo
            i = 0
            n = len(datos)
            while True:
                izq = 2 * i + 1
                der = izq + 1
                menor = i
                if izq < n and datos[izq] < datos[menor]:
                    menor = izq
                if der < n and datos[der] < datos[menor]:
                    menor = der
                if menor == i:
                    break
                datos[i], datos[menor] = datos[menor], datos[i]
                i = menor
        return minimo
