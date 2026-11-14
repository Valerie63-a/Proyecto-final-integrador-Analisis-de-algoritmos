from c2_tabla_hash.tabla_hash import TablaHash


def medir_costo_acumulado(n):
    tabla = TablaHash()
    for clave in range(n):
        tabla.insertar(clave, clave)
    return tabla.costo_acumulado, tabla.num_redimensionamientos


def main():
    print(f"{'n':>8} {'costo':>10} {'costo/n':>8} {'3n':>10} {'dup.':>5}")
    n = 1000
    for _ in range(8):  # 8 tamaños en progresión geométrica
        costo, duplicaciones = medir_costo_acumulado(n)
        print(f"{n:>8} {costo:>10} {costo / n:>8.3f} {3 * n:>10} {duplicaciones:>5}")
        n *= 2


if __name__ == "__main__":
    main()
