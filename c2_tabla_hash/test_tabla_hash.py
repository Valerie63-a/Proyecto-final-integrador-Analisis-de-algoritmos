from c2_tabla_hash.tabla_hash import TablaHash
from datos.generador import generar_vehiculos, EstadoVehiculo


def test_insertar_y_obtener():
    tabla = TablaHash()
    tabla.insertar(10, "a")
    tabla.insertar(20, "b")
    assert tabla.obtener(10) == "a"
    assert tabla.obtener(99) is None
    assert len(tabla) == 2


def test_actualizar_no_crece():
    tabla = TablaHash()
    tabla.insertar(1, "a")
    tabla.insertar(1, "b")
    assert len(tabla) == 1
    assert tabla.obtener(1) == "b"
    assert tabla.costo_acumulado == 1


def test_duplicacion_de_capacidad():
    tabla = TablaHash(4)
    for clave in range(4):
        tabla.insertar(clave, clave)
    assert tabla.capacidad == 4
    tabla.insertar(4, 4)
    assert tabla.capacidad == 8
    assert tabla.num_redimensionamientos == 1
    assert tabla.costo_acumulado == 9  # 5 inserciones + 4 reubicaciones


def test_no_pierde_claves_tras_muchas_duplicaciones():
    tabla = TablaHash()
    for clave in range(0, 5000, 3):
        tabla.insertar(clave, clave * 2)
    for clave in range(0, 5000, 3):
        assert tabla.obtener(clave) == clave * 2


def test_costo_acumulado_menor_o_igual_a_3n():
    for n in [1, 5, 100, 1025, 5000]:
        tabla = TablaHash()
        for clave in range(n):
            tabla.insertar(clave, clave)
        assert tabla.costo_acumulado <= 3 * n


def test_costo_exacto_en_el_peor_n():
    tabla = TablaHash()
    for clave in range(1025):
        tabla.insertar(clave, clave)
    assert tabla.costo_acumulado == 3069  # 1025 + (4+8+...+1024)


def test_estados_de_vehiculos():
    tabla = TablaHash()
    vehiculos = generar_vehiculos(50)
    for identificador, estado in vehiculos:
        tabla.insertar(identificador, estado)
    for identificador, estado in vehiculos:
        assert tabla.obtener(identificador) == estado
    tabla.insertar(3, EstadoVehiculo(1.0, 2.0, 99))  # el vehículo 3 se mueve
    assert tabla.obtener(3).carga == 99
    assert len(tabla) == 50

def test_capacidad_inicial_debe_ser_potencia_de_dos():
    import pytest
    with pytest.raises(ValueError):
        TablaHash(capacidad_inicial=6)


def test_claves_de_paso_potencia_de_dos_no_se_amontonan():
    # Con el módulo (bits bajos) 4096 claves de paso 1024 caían en 4 cubetas
    # (cadena de 1024). Con el desplazamiento (bits altos) se reparten.
    for paso in (16, 256, 1024):
        tabla = TablaHash()
        for k in range(4096):
            tabla.insertar(k * paso, k)
        assert max(len(c) for c in tabla.cubetas) <= 8
        assert all(tabla.obtener(k * paso) == k for k in range(4096))
