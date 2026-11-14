#C2: sensibilidad de la función hash a la estructura de las llaves.

#Hipótesis: con la función corregida, ((k·2654435761) mod 2^32) >> (32 - p),
#la cadena máxima no depende del paso de las llaves. Con la versión anterior
#(... mod capacidad, bits bajos) las llaves de paso 2^j colisionaban: con
#paso 16, 256 y 1024 la cadena máxima era 16, 256 y 1024. Ahora es 2.

from c2_tabla_hash.tabla_hash import TablaHash


def main():
    n = 4096
    print(f"{'paso':>6} {'capacidad':>10} {'cadena máx.':>12} {'costo/n':>8}")
    for paso in (1, 3, 16, 256, 1024):
        tabla = TablaHash()
        for k in range(n):
            tabla.insertar(k * paso, k)
        cadena = max(len(c) for c in tabla.cubetas)
        print(f"{paso:>6} {tabla.capacidad:>10} {cadena:>12} {tabla.costo_acumulado / n:>8.3f}")


if __name__ == "__main__":
    main()
