import os
import struct


class DiscoSimulado:
    # Disco de bloques de tamaño fijo sobre un archivo binario.
    # Cada bloque guarda hasta B registros; cada registro son len(formato) números
    # (formato de struct, un carácter por campo, p. ej. "qdddd").
    # Único punto de acceso al archivo: cuenta cada leer_bloque y escribir_bloque.

    def __init__(self, ruta, registros_por_bloque, formato="qdddd"):
        self.ruta = ruta
        self.B = registros_por_bloque
        self.campos = len(formato)
        self._bloque = struct.Struct("<I" + formato * registros_por_bloque)
        self._vacio = (0,) * (self.campos * registros_por_bloque)
        self._archivo = open(ruta, "w+b")
        self.lecturas = 0
        self.escrituras = 0
        self.proximo_bloque = 0  # asignador secuencial de bloques libres

    def reservar(self, cantidad):
        # Reserva 'cantidad' bloques consecutivos y devuelve el índice del primero.
        primero = self.proximo_bloque
        self.proximo_bloque += cantidad
        return primero

    def reiniciar_contadores(self):
        self.lecturas = 0
        self.escrituras = 0

    def escribir_bloque(self, i, datos):
        if len(datos) > self.B:
            raise ValueError("el bloque admite como máximo B registros")
        plano = [v for registro in datos for v in registro]
        plano.extend(self._vacio[: self.campos * (self.B - len(datos))])
        self._archivo.seek(i * self._bloque.size)
        self._archivo.write(self._bloque.pack(len(datos), *plano))
        self.escrituras += 1

    def leer_bloque(self, i):
        self._archivo.seek(i * self._bloque.size)
        crudo = self._archivo.read(self._bloque.size)
        if len(crudo) < self._bloque.size:
            raise IndexError(f"el bloque {i} no existe")
        self.lecturas += 1
        valores = self._bloque.unpack(crudo)
        cuenta = valores[0]
        c = self.campos
        return [valores[1 + k * c: 1 + (k + 1) * c] for k in range(cuenta)]

    def cerrar(self, borrar=True):
        self._archivo.close()
        if borrar and os.path.exists(self.ruta):
            os.remove(self.ruta)
