class TablaHash:
    #Tabla hash con encadenamiento y duplicación de capacidad.
    #Función hash: hashing multiplicativo de Knuth. Como la capacidad es 2^p,
    #el índice son los p bits MÁS significativos del producto de 32 bits
    #(desplazamiento a la derecha), no los menos significativos (módulo).

    def __init__(self, capacidad_inicial=4):
        if capacidad_inicial < 1 or capacidad_inicial & (capacidad_inicial - 1):
            raise ValueError("la capacidad inicial debe ser una potencia de 2")
        self.capacidad = capacidad_inicial
        self.bits = capacidad_inicial.bit_length() - 1   # capacidad = 2^bits
        self.tamano = 0
        self.cubetas = [[] for _ in range(capacidad_inicial)]
        self.costo_acumulado = 0
        self.num_redimensionamientos = 0

    @staticmethod
    def _indice(clave, bits):
        #h(k) = ((k · A) mod 2^32) >> (32 - p), con A = 2654435761 ≈ 2^32/φ.
        #El desplazamiento conserva los bits altos del producto, que dependen
        #de todos los bits de la clave; el módulo por 2^p conservaría solo los
        #bits bajos y las claves de paso 2^j caerían en 2^p / 2^j cubetas.
        if bits == 0:
            return 0
        return ((clave * 2654435761) & 0xFFFFFFFF) >> (32 - bits)

    def insertar(self, clave, valor):
        #Inserta o actualiza. Duplica la capacidad si la tabla está llena.
        cubeta = self.cubetas[self._indice(clave, self.bits)]
        for posicion in range(len(cubeta)):
            if cubeta[posicion][0] == clave:
                cubeta[posicion] = (clave, valor)  # actualización: no crece
                return

        if self.tamano == self.capacidad:
            self._duplicar()
            cubeta = self.cubetas[self._indice(clave, self.bits)]

        cubeta.append((clave, valor))
        self.tamano += 1
        self.costo_acumulado += 1

    def obtener(self, clave, defecto=None):
        cubeta = self.cubetas[self._indice(clave, self.bits)]
        for clave_guardada, valor in cubeta:
            if clave_guardada == clave:
                return valor
        return defecto

    def _duplicar(self):
        nueva_capacidad = 2 * self.capacidad
        nuevos_bits = self.bits + 1
        nuevas_cubetas = [[] for _ in range(nueva_capacidad)]
        for cubeta in self.cubetas:
            for clave, valor in cubeta:
                nuevas_cubetas[self._indice(clave, nuevos_bits)].append((clave, valor))
                self.costo_acumulado += 1  # cada reubicación cuesta 1
        self.cubetas = nuevas_cubetas
        self.capacidad = nueva_capacidad
        self.bits = nuevos_bits
        self.num_redimensionamientos += 1

    def __len__(self):
        return self.tamano
